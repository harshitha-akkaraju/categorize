import fasttext
import os

def get_cbow_model(regenerate=False):
    cbow_model_file_path = './models/cbow_model.bin'
    if regenerate:
        print("regenerating the cbow model...")
        
        data_file_path = "./data/the_daily_data.txt"
        cbow_model = fasttext.train_unsupervised(data_file_path, model='cbow')
        cbow_model.save_model(cbow_model_file_path)
    
    if os.path.exists(cbow_model_file_path):
        model = fasttext.load_model(cbow_model_file_path)
        return model
    
    return None


def main():
   cbow_model = get_cbow_model()
   if cbow_model == None:
       print("something went wrong...")
       exit()
    

if __name__ == "__main__":
    main()

