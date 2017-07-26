import tensorflow as tf
import numpy as np

class Seq2Seq:
    def __init__(self, xseq_len, yseq_len, xvocab_size, yvocab_size,
                 lstm_cell_size, lstm_layers, embed_size, epoch_n):
        
        self.xseq_len = xseq_len 
        self.yseq_len = yseq_len 
        self.xvocab_size = xvocab_size
        self.yvocab_size = yvocab_size
        self.lstm_cell_size = lstm_cell_size
        self.lstm_layers = lstm_layers
        self.embed_size = embed_size 
        
        self.epoch_n = epoch_n
        self.lr = 0.01  
        
        self.global_iteration=0

    def create_placeholder(self):
        # Clean Graph:
        tf.reset_default_graph()
        
        # Placeholders:                       None:Represents batch_size
        self.enc_ip = [ tf.placeholder(shape=[None,], 
                        dtype=tf.int64, 
                        name='ei_{}'.format(t)) for t in range(self.xseq_len) ]
        self.labels = [ tf.placeholder(shape=[None,], 
                        dtype=tf.int64, 
                        name='l_{}'.format(t)) for t in range(self.yseq_len) ]
        
        # Decoder inputs : 'GO' + [ y1, y2, ... y_t-1 ]
        self.dec_ip = [ tf.zeros_like(self.enc_ip[0], dtype=tf.int64, name='GO') ] + self.labels[:-1]
        
    def build_graph(self):
        #Build Encoder-Decoder:
        lstm = tf.contrib.rnn.BasicLSTMCell(self.lstm_cell_size)
        
        lstm = tf.contrib.rnn.MultiRNNCell([lstm]*self.lstm_layers)
        
        with tf.variable_scope('decoder') as scope:
          self.decode_outputs, _ = tf.contrib.legacy_seq2seq.embedding_rnn_seq2seq(self.enc_ip, self.dec_ip,
                                                                                 lstm, self.xvocab_size,
                                                                                 self.yvocab_size,self.embed_size,
                                                                                 feed_previous =False)
          scope.reuse_variables() #sharing parameter b/w train and test decoders
          self.decode_outputs_test, _ = tf.contrib.legacy_seq2seq.embedding_rnn_seq2seq(self.enc_ip, self.dec_ip,
                                                                                      lstm, self.xvocab_size,
                                                                                      self.yvocab_size,self.embed_size,
                                                                                      feed_previous =True)
        
        #Loss & Optimisation
        loss_weights = [ tf.ones_like(label, dtype=tf.float32) for label in self.labels ]
        self.loss_train = tf.contrib.legacy_seq2seq.sequence_loss(self.decode_outputs, self.labels, loss_weights, self.yvocab_size)
        self.loss_valid = tf.contrib.legacy_seq2seq.sequence_loss(self.decode_outputs_test, self.labels, loss_weights, self.yvocab_size)
        
        tf.summary.scalar("Train_Loss", self.loss_train)
        tf.summary.scalar("Valid_Loss", self.loss_valid)
        self.merged_summary_op = tf.summary.merge_all()
        
        self.optimizer = tf.train.AdamOptimizer(learning_rate=self.lr).minimize(self.loss_train)
        
    def get_batches(self, inp, batch_size=200):
			x, y = inp[0], inp[1]
			n_batches = len(x)//batch_size
			x, y = x[:n_batches*batch_size], y[:n_batches*batch_size]
			for ii in range(0, len(x), batch_size):
				yield x[ii:ii+batch_size], y[ii:ii+batch_size]
    
    def get_feed(self, X, Y):
            feed_dict = {self.enc_ip[t]: X[t] for t in range(self.xseq_len)}
            if Y is not None:
              feed_dict.update({self.labels[t]: Y[t] for t in range(self.yseq_len)})
            return feed_dict
    
    def eval_valid_loss(self, sess, valid_set):
        losses = []
        for valid_batch in self.get_batches(valid_set):
            batchX, batchY = valid_batch
            feed_dict = self.get_feed(batchX, batchY)
            summary, outputs, loss = sess.run([self.merged_summary_op, self.decode_outputs, self.loss_valid], feed_dict)
            self.summary_writer.add_summary(summary, self.global_iteration)
            
            losses.append(loss)
        print 'X: ',batchX[0]
        print 'Prediction: ',np.argmax(np.array(outputs).transpose([1,0,2]), axis=2) [0]
        print 'Y: ',batchY[0]
        print 
        return np.mean(losses)
            
    def train_batch(self, sess, train_set_batch):        
        batchX, batchY = train_set_batch
        feed_dict = self.get_feed(batchX, batchY)
        summary, _, loss_v = sess.run([self.merged_summary_op, self.optimizer, self.loss_train], feed_dict)
        self.summary_writer.add_summary(summary, self.global_iteration)
        
        return loss_v
        
    
    def train(self, train_set, valid_set):
        self.create_placeholder()
        self.build_graph()       
 
        sess = tf.Session()
        sess.run(tf.global_variables_initializer() )
        self.summary_writer = tf.summary.FileWriter('/tmp/SpellCorrector', graph=tf.get_default_graph())
        
        print('Start Training...')
        for epoch_i in range(self.epoch_n):
            for iteration,train_set_batch in enumerate(self.get_batches(train_set), 1):
                train_loss = self.train_batch(sess, train_set_batch)
                
                # Print Results:
                if(iteration%5==0):
                    print("Iteration:  ",iteration)
                    print("Train Loss: ",train_loss)
                    print("Valid Loss: ",self.eval_valid_loss(sess, valid_set))
                    print 
                self.global_iteration+=1
        print('Training Completed...')
        
        return sess        

    def demo(self, X, Ycap, Y):
       import data_util
       for i in range(len(X)):
         print data_util.indexes2string(X[i]),'  ',data_util.indexes2string(Ycap[i]),'  ', data_util.indexes2string(Y[i])

    def predict(self, sess, test_set_batch):
			batchX = test_set_batch
			feed_dict = self.get_feed(batchX, None)

			output_ = sess.run(self.decode_outputs_test, feed_dict)
			output_ = np.array(output_).transpose([1,0,2])
			print np.shape(output_)
			return np.argmax(output_, axis=2)


    def test(self, sess, test_set):
        input_, prediction, output_ = [], [], []
        for X,Y in self.get_batches(test_set):
            input_.extend(X), output_.extend(Y)
            prediction.extend(self.predict(sess, X) )
        self.demo(input_, prediction, output_)
   

