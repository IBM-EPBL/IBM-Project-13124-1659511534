#Building a model based on the above defined function
model=load_CNN(6) #Number of Columns/Outputs
model.compile(loss='categorical_crossontropy',optimizer=Adam(lr=0.001),metrics=['accuracy'])
model.summary #to print model summary
weights=model.get_weights() #to get the weighs from model

#some arrays to store the result of each model
histories_acc=[]
histories_val_acC=[]
histories_loss=[]
histories_val_loss=[]
model.set_weights(weights)
h=model.fit(X_train, y_train,
            batch_size=16,
            epochs=7,
            verbose=l,
            callbacks=[early_stop_loss],
            shuffle=True,
            validat1on_data=(X_test, y_test))
model.summary()#to print model summary