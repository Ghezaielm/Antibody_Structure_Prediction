##### Data processing #####################################################################
# Methods: 
#    - addBcmFeatures: Add biochemical features such as polarity, charge, and residue ID
#    - scale: MinMaxScale the data in (0,1) range
#    - slice: Define temporal windows (rotamers) of 2xWS length
###########################################################################################

class processData(monitor):
    
    def __init__(self,data): 
        self.data = data
        self.base = {"A":1,"R":16,"N":13,"D":18,"C":3,"E":19,"Q":14,"G":0,"H":17,"I":6,"L":5,"K":15,"M":7,"F":9,"P":4,"S":10,"T":11,"W":8,"Y":12,"V":2}

        
    @monitor.timer
    def addBcmFeatures(self): 
        for chain in self.data:
            chain["Residue"] = [self.base[i] for i in chain["Residue"]]
            chain["isPolar"] = [1 if i not in [k for k in range(10,15)] else 0 for i in chain["Residue"]]
            chain["isPositive"] = [1 if i  in [k for k in range(15,18)] else 0 for i in chain["Residue"]]
            chain["isNegative"] = [1 if i  in [k for k in range(18,20)] else 0 for i in chain["Residue"]]
            chain["isAromatic"] = [1 if i  in [8,9,12] else 0 for i in chain["Residue"]]
            chain['isPhosphorylable'] = [1 if i  in [10,11,12] else 0 for i in chain["Residue"]]
            chain["isHydrophobic"] = [1 if i  in [1,6,5,4,2] else 0 for i in chain["Residue"]]
            chain["hasThiol"] = [1 if i  in [7,3] else 0 for i in chain["Residue"]]
            
    @monitor.timer         
    def addPolyFeatures(self):
        self.augmented = []
        for chain in self.data: 
            cols = [col for col in chain.columns]
            poly = PolynomialFeatures(2)
            augmented = poly.fit_transform(chain)
            augmented = pd.concat([chain,pd.DataFrame(augmented)],axis=1,join='inner')
            #augmented = pd.DataFrame(augmented, columns = cols+[str(i) for i in range(augmented.shape[1]-len(cols))])
            #print(chain["isPolar"],augmented["isPolar"])
            self.augmented.append(augmented)
        self.data = self.augmented.copy() 
        del self.augmented
            
            
            
    def scale(array):
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled = scaler.fit_transform(array)
        return scaled

    @monitor.timer
    def slice(self,ws=5):
        self.ws, X_data, y_data = ws,[],[]  
        for chain in self.data:
            data = chain
#             print(data.columns)
#             input_features = []
#             # Recompute correlation
#             corr = chain.corr()
#             # Generate a mask for the upper triangle
#             mask = np.triu(np.ones_like(corr, dtype=np.bool))

#             # Set up the matplotlib figure
#             f, ax = plt.subplots(figsize=(11, 9))

#             # Generate a custom diverging colormap
#             cmap = sns.diverging_palette(50, 90, as_cmap=True)

#             # Draw the heatmap with the mask and correct aspect ratio
#             sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, center=0,
#             square=True, linewidths=.5, cbar_kws={"shrink": .5})
#             plt.show()
            target_features = ["Residue"]
            for idx in range(self.ws,data.shape[0]-self.ws):
                X_data.append(processData.scale(data.iloc[idx-self.ws:idx,:].values))
                y_data.append(data.filter(target_features).iloc[idx:idx+self.ws,:].values)

        self.X = np.array(X_data)
        self.y = np.array(y_data)
        if len(self.y.shape)!=2:
            pass
        else:
            self.y = self.y.reshape(self.y.shape[0],self.y.shape[1],1)
