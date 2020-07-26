from init import launch

paths = ["4ydi.pdb","4ydj.pdb","4ydk.pdb","4ydl.pdb","4ydv.pdb"]
init = launch(paths)
init._parse()
init._process()
init._Model(100,100,bs=200,epochs=100)
