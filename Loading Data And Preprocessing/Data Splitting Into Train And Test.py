print(X_data)
print(Y_data)

X=np.array(X_data)
Y=np.array(Y_data)

print("x-shape",X.shape,"y shape",Y.shape)

X=X.astype('float32')/255.0
y_cat=to_categorical(Y_data,len(subfolders))

print("X shape",X,"y_cat shape",y_cat)
print("X shape",X.shape,"y_cat shape",y_cat.shape)

X_train,X_test,y_train,y_test=train_test_split(X,y_cat,test_size=0.2)
print("The model has "+str(len(X_train))+" inputs")
