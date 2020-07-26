####### LSTM Model #########################################
# Methods:
#    - splitData: split the dataset into training and test set
#    - setModel: define model architecture
#    - train: train the model
#    - fineTune: finetune the model
#    - showMetrics: show training and testing metrics
############################################################

class LSTM_AE(monitor):
    
    def __init__(self,X,y): 
        self.X,self.y = X,y
    
    def splitData(self,test_size=0.10): 
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=test_size,
                                                             random_state=42) 
    
    @monitor.timer
    def setModel(self,l1,l2):
        self.model = Sequential()
        self.model.add(Conv1D(filters=128, kernel_size=3, activation='relu', input_shape=(self.X.shape[1],self.X.shape[2])))
        self.model.add(Conv1D(filters=128, kernel_size=3, activation='relu'))
        self.model.add(MaxPooling1D(pool_size=1))
        self.model.add(Flatten())
        #self.model.add(LSTM(l1, activation='relu', input_shape=(self.X.shape[1],self.X.shape[2]), return_sequences=True))
        #self.model.add(LSTM(l2, activation='relu', return_sequences=False))
        self.model.add(RepeatVector(self.X.shape[1]))
        self.model.add(Dropout(0.4))
        self.model.add(LSTM(l2, activation='relu', return_sequences=True))
        self.model.add(LSTM(l1, activation='relu', return_sequences=True))
        self.model.add(TimeDistributed(Dense(self.y.shape[2])))
        self.model.compile(optimizer='adam', loss='mse',metrics = ['mse'])
        self.model.summary()
        
    @monitor.timer
    def train(self,epochs,bs): 
        self.filepath1 = os.path.join(os.getcwd(),"Run1.hdf5")
        checkpoint = ModelCheckpoint(self.filepath1, monitor="val_mse", verbose = 1, save_best_only = True, mode = 'min')
        callbacks_list = [checkpoint]
        self.history = self.model.fit(self.X_train,self.y_train,epochs=epochs,batch_size=bs,verbose=1,validation_data = (self.X_test,self.y_test),callbacks=callbacks_list)
        
    def fineTune(self,epochs,bs,lr=1e-3):
        self.model.load_weights(self.filepath1)
        self.filepath2 = os.path.join(os.getcwd(),"Run2.hdf5")
        self.model.compile(optimizer=keras.optimizers.Adam(lr), loss='mse',metrics = ['mse'])
        checkpoint = ModelCheckpoint(self.filepath2, monitor="val_mse", verbose = 1, save_best_only = True, mode = 'min')
        callbacks_list = [checkpoint]
        self.history = self.model.fit(self.X_train,self.y_train,epochs=epochs,batch_size=bs,verbose=1,validation_data = (self.X_test,self.y_test),callbacks=callbacks_list)
        
        
    def showMetrics(self,title): 
        plt.style.use("ggplot")
        f = plt.figure(figsize=(10,10))
        ax,ax1,ax2,ax3 = f.add_subplot(221),f.add_subplot(222),f.add_subplot(223),f.add_subplot(224)
        
        ax.plot(self.history.history["loss"])
        ax1.plot(self.history.history["val_loss"])
        ax2.plot(self.history.history["mse"])
        ax3.plot(self.history.history["val_mse"])
        f.suptitle("{} Validation metrics 70/30".format(title),fontsize=15)
        ax.set_title("Training loss")
        ax1.set_title("Testing loss")
        ax2.set_title("Training mse")
        ax3.set_title("Testing mse")
        print(self.y_test)
        print(self.model.predict(self.X_test))
