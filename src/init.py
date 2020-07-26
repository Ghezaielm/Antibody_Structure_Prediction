from monitor import monitor


class launch(monitor): 
    
    def __init__(self,path): 
        self.paths = path
    
    @monitor.timer
    def _parse(self): 
        self.parsed = []
        for structure in self.paths:
            o = parseStructure(structure)
            o.getStructure()
            o.rotateStructure()
            o.getFeatures()
            for parsed in o.data:
                self.parsed.append(parsed)

    @monitor.timer        
    def _process(self):
        o = processData(self.parsed)
        o.addBcmFeatures()
        o.addPolyFeatures()
        o.slice()
        self.X = o.X
        self.y = o.y
        print("Input shape: {}\n Output shape: {}".format(o.X.shape,o.y.shape))
    
    def _Model(self,l1,l2,epochs=5,bs=10):
        o = LSTM_AE(self.X,self.y)
        o.splitData()
        o.setModel(l1,l2)
        o.train(epochs,bs)
        o.showMetrics("Run 1")
        o.fineTune(epochs=50,bs=200)
        o.showMetrics("Fine tuning")
        self.result = o.copy()
        
