from ryu.controller import ofp_event

from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER

from ryu.controller.handler import set_ev_cls

from ryu.lib import hub



import switch, switchm

from datetime import datetime

import pickle, os

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler

from sklearn.neural_network import MLPClassifier

from sklearn.metrics import confusion_matrix, accuracy_score



class SimpleMonitor13(switchm.SimpleSwitch13):



    def __init__(self, *args, **kwargs):

        super(SimpleMonitor13, self).__init__(*args, **kwargs)

        self.datapaths = {}

        self.monitor_thread = hub.spawn(self._monitor)



        start = datetime.now()



        self.flow_training()



        end = datetime.now()

        print("Training time: ", (end-start))



    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])

    def _state_change_handler(self, ev):

        datapath = ev.datapath

        if ev.state == MAIN_DISPATCHER:

            if datapath.id not in self.datapaths:

                self.logger.debug('register datapath: %016x', datapath.id)

                self.datapaths[datapath.id] = datapath

        elif ev.state == DEAD_DISPATCHER:

            if datapath.id in self.datapaths:

                self.logger.debug('unregister datapath: %016x', datapath.id)

                del self.datapaths[datapath.id]



    def _monitor(self):

        while True:

            for dp in self.datapaths.values():

                self._request_stats(dp)

            hub.sleep(10)



            self.flow_predict()



    def _request_stats(self, datapath):

        self.logger.debug('send stats request: %016x', datapath.id)

        parser = datapath.ofproto_parser



        req = parser.OFPFlowStatsRequest(datapath)

        datapath.send_msg(req)



    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)

    def _flow_stats_reply_handler(self, ev):

        timestamp = datetime.now()

        timestamp = timestamp.timestamp()



        file0 = open("PredictFlowStatsfile.csv","w")

        file0.write('timestamp,datapath_id,flow_id,ip_src,tp_src,ip_dst,tp_dst,ip_proto,icmp_code,icmp_type,flow_duration_sec,flow_duration_nsec,idle_timeout,hard_timeout,flags,packet_count,byte_count,packet_count_per_second,packet_count_per_nsecond,byte_count_per_second,byte_count_per_nsecond\n')

        body = ev.msg.body

        icmp_code = -1

        icmp_type = -1

        tp_src = 0

        tp_dst = 0



        for stat in sorted([flow for flow in body if (flow.priority == 1)], key=lambda flow: (flow.match['eth_type'], flow.match['ipv4_src'], flow.match['ipv4_dst'], flow.match['ip_proto'])):



            ip_src = stat.match['ipv4_src']

            ip_dst = stat.match['ipv4_dst']

            ip_proto = stat.match['ip_proto']



            if stat.match['ip_proto'] == 1:

                icmp_code = stat.match['icmpv4_code']

                icmp_type = stat.match['icmpv4_type']



            elif stat.match['ip_proto'] == 6:

                tp_src = stat.match['tcp_src']

                tp_dst = stat.match['tcp_dst']



            elif stat.match['ip_proto'] == 17:

                tp_src = stat.match['udp_src']

                tp_dst = stat.match['udp_dst']



            flow_id = str(ip_src) + str(tp_src) + str(ip_dst) + str(tp_dst) + str(ip_proto)



            try:

                packet_count_per_second = stat.packet_count/stat.duration_sec

                packet_count_per_nsecond = stat.packet_count/stat.duration_nsec

            except:

                packet_count_per_second = 0

                packet_count_per_nsecond = 0



            try:

                byte_count_per_second = stat.byte_count/stat.duration_sec

                byte_count_per_nsecond = stat.byte_count/stat.duration_nsec

            except:

                byte_count_per_second = 0

                byte_count_per_nsecond = 0



            file0.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n"

                        .format(timestamp, ev.msg.datapath.id, flow_id, ip_src, tp_src, ip_dst, tp_dst,

                                stat.match['ip_proto'], icmp_code, icmp_type,

                                stat.duration_sec, stat.duration_nsec,

                                stat.idle_timeout, stat.hard_timeout,

                                stat.flags, stat.packet_count, stat.byte_count,

                                packet_count_per_second, packet_count_per_nsecond,

                                byte_count_per_second, byte_count_per_nsecond))



        file0.close()



    def flow_training(self):

        self.logger.info("MLP Training ...")

        modelDB = 'mlp_model_detech.pkl'



        if os.path.exists(modelDB):

            # Load the saved model from file

            print("File exist, loading model")

            with open(modelDB, 'rb') as file:

                self.flow_model = pickle.load(file)

        else:

            print("File does not exist, training model")



            flow_dataset = pd.read_csv('FlowStatsfile.csv')



            # Normalize the data

            flow_dataset.iloc[:, 2] = flow_dataset.iloc[:, 2].str.replace('.', '')

            flow_dataset.iloc[:, 3] = flow_dataset.iloc[:, 3].str.replace('.', '')

            flow_dataset.iloc[:, 5] = flow_dataset.iloc[:, 5].str.replace('.', '')



            X_flow = flow_dataset.iloc[:, :-1].values

            X_flow = X_flow.astype('float64')



            scaler = StandardScaler()

            X_flow = scaler.fit_transform(X_flow)



            y_flow = flow_dataset.iloc[:, -1].values



            X_flow_train, X_flow_test, y_flow_train, y_flow_test = train_test_split(X_flow, y_flow, test_size=0.25, random_state=0)



            # Construct the MLP model

            self.flow_model = MLPClassifier(hidden_layer_sizes=(128, 64), activation='relu', solver='adam', random_state=1, max_iter=500)

            self.flow_model.fit(X_flow_train, y_flow_train)



            y_flow_pred = self.flow_model.predict(X_flow_test)

            y_flow_pred_train = self.flow_model.predict(X_flow_train)



            with open(modelDB, 'wb') as file:

                pickle.dump(self.flow_model, file)



            self.logger.info("------------------------------------------------------------------------------")



            self.logger.info("Confusion Matrix")

            cm = confusion_matrix(y_flow_test, y_flow_pred)

            self.logger.info(cm)



            acc = accuracy_score(y_flow_test, y_flow_pred)



            acc_train = accuracy_score(y_flow_train, y_flow_pred_train)

            print("Training Accuracy: ", acc_train)



            self.logger.info("Success Accuracy = {0:.2f} %".format(acc * 100))

            fail = 1.0 - acc

            self.logger.info("Fail Accuracy = {0:.2f} %".format(fail * 100))

            self.logger.info("------------------------------------------------------------------------------")



    def flow_predict(self):

        try:

            predict_flow_dataset = pd.read_csv('PredictFlowStatsfile.csv')

            raw_data = predict_flow_dataset.copy()

            predict_flow_dataset.iloc[:, 2] = predict_flow_dataset.iloc[:, 2].str.replace('.', '')

            predict_flow_dataset.iloc[:, 3] = predict_flow_dataset.iloc[:, 3].str.replace('.', '')

            predict_flow_dataset.iloc[:, 5] = predict_flow_dataset.iloc[:, 5].str.replace('.', '')



            X_predict_flow = predict_flow_dataset.iloc[:, :].values

            X_predict_flow = X_predict_flow.astype('float64')



            scaler = StandardScaler()

            X_predict_flow = scaler.fit_transform(X_predict_flow)



            y_flow_pred = self.flow_model.predict(X_predict_flow)

            # Nếu file chưa tồn tại → ghi tiêu đề

            file_exist = os.path.isfile('ResultFlowPrediction.csv')



            raw_data['prediction'] = y_flow_pred

            raw_data.to_csv('ResultFlowPrediction.csv', mode='a', header=not file_exist, index=False)

            legitimate_traffic = 0

            ddos_traffic = 0



            for i in y_flow_pred:

                if i == 0:

                    legitimate_traffic += 1

                else:

                    ddos_traffic += 1

                    victim = int(predict_flow_dataset.iloc[i, 5]) % 20



            self.logger.info("------------------------------------------------------------------------------")

            if (legitimate_traffic / len(y_flow_pred) * 100) > 80:

                self.logger.info("Legitimate traffic ...")

            else:

                self.logger.info("DDoS traffic ...")

                self.logger.info("Victim is host: h{}".format(victim))

                self.mitigation = 1

            self.logger.info("------------------------------------------------------------------------------")



            file0 = open("PredictFlowStatsfile.csv", "w")

            file0.write('timestamp,datapath_id,flow_id,ip_src,tp_src,ip_dst,tp_dst,ip_proto,icmp_code,icmp_type,flow_duration_sec,flow_duration_nsec,idle_timeout,hard_timeout,flags,packet_count,byte_count,packet_count_per_second,packet_count_per_nsecond,byte_count_per_second,byte_count_per_nsecond\n')

            file0.close()



        except:

            pass