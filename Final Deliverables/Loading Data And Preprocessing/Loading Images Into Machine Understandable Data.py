X_data=[]
Y_data=[]
id_no=0

found=[]

for paths in subfolders:
    files = glob.glob(paths+ "/*.jpg")
    found.append((paths.split('||')[-2],paths.split('||')[-1]))

    for myFile in files:
        img=Image.open(myFile)
        img=img.resize((224,224),Image.ANTIALIAS)
        img=np.array(img)
        if img.shape==(224,224,3):
            X_data.append(img)
            Y_data.append(id_no)
    id_no+=1
