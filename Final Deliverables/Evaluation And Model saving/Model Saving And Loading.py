model_json=model.to_json(0 
with open("final_model.json","w") as json_file:
   json_file.write(model_json) 

model.save_weights("final_model.h5") 
print("Saved model to disk")