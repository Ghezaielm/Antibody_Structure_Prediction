  
    
####### Parse PDB structures ##################################################
# Methods: 
#    - getStructure: parse the PDB file 
#    - rotateStructure: normalize the 3D structure so that AA1 is the ref
#    - getFeatures: create several features such as torsion angles and bfactors
##############################################################################

class parseStructure(monitor):
    
    def __init__(self,ID):
        self.parser = PDB.PDBParser()
        self.io = PDB.PDBIO()
        
        self.id = ID
        
    
    @monitor.timer
    def getStructure(self): 
        self.structure = self.parser.get_structure(self.id.split("i")[0],self.id)
     
    @monitor.timer
    def rotateStructure(self): 
        # We define a rotation matrix 
        rotation_matrix = PDB.rotmat(PDB.Vector([0, 0, 0]), PDB.Vector([0, 0, 0]))
        
        # Fetch the reference atom 
        for atom in self.structure.get_atoms():
            C1 = atom.coord.copy()
            break
            
        # Normalize
        self.rotated = self.structure.copy()
        for model in self.rotated:
            for chain in model:
                for residue in chain:
                    for atom in residue:
                        # Rotate the atom such that it points to the origin
                        # Then translate by substracting the reference coordinates
                        atom.transform(rotation_matrix, -C1)
                        
    @monitor.timer
    def getFeatures(self):
        self.chains = {}
        ppb=PPBuilder()
        # The ppb object is not a generator 
        # So we can use enumerate
        self.data = []
        
        for id_chain,chain in enumerate(ppb.build_peptides(self.rotated)):
            curr = pd.DataFrame()
            # Store the columns
            curr["Residue"]=[i for i in chain.get_sequence()][1:-4]
            curr["X"] = [atom.get_coord()[0] for atom in chain.get_ca_list()] [1:-4]
            curr["Y"] = [atom.get_coord()[1] for atom in chain.get_ca_list()] [1:-4] 
            curr["Z"] = [atom.get_coord()[2] for atom in chain.get_ca_list()] [1:-4] 
            curr["Phi"] = [angle[0] for angle in chain.get_phi_psi_list()][1:-4]
            curr["Psi"] = [angle[1] for angle in chain.get_phi_psi_list()][1:-4]
            curr["Tau"] = [angle for idx,angle in enumerate(chain.get_tau_list())][1:-1]
            curr["Theta"] = [angle for idx,angle in enumerate( chain.get_theta_list())][1:-2]
            curr["B_Factor_1"]= [atom.get_anisou()[0] for atom in chain.get_ca_list()] [1:-4]
            curr["B_Factor_2"]= [atom.get_anisou()[1] for atom in chain.get_ca_list()] [1:-4]
            curr["B_Factor_3"]= [atom.get_anisou()[2] for atom in chain.get_ca_list()] [1:-4]
            curr["B_Factor_4"]= [atom.get_anisou()[3] for atom in chain.get_ca_list()] [1:-4]
            curr["B_Factor_5"]= [atom.get_anisou()[4] for atom in chain.get_ca_list()] [1:-4]
            curr["B_Factor_6"]= [atom.get_anisou()[5] for atom in chain.get_ca_list()] [1:-4]
            self.data.append(curr)

