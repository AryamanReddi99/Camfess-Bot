import csv
import facebook_scraper as fb
import datetime
import pandas as pd

fn = 'database/pasta.csv'

class pasta_db():
    def __init__(self,filename):
        self.filename=filename
        self.df = None
        self.headers = ["id","pasta","date","used"]
        self.reset_df = pd.DataFrame({"id":[],
                        "pasta":[],
                        "date":[],
                        "used":[]}).set_index("id")
    def read_df(self):
        """
        create df from csv
        """
        self.df = pd.read_csv(self.filename,index_col="id")
    def force_reset(self):
        """
        force entries to 0
        """
        self.reset_df.to_csv(self.filename)
        print("resetting pasta database...")
    def reset_file(self):
        """
        reset file to no entries if too large
        """
        self.read_df()
        self.num_rows = len(self.df.index)
        if self.num_rows > 1000:
            self.reset_df.to_csv(self.filename)
            print("resetting pasta database...")
    def add_pasta(self):
        """
        append new posts to csv
        """
        self.read_df()
        posts_raw = fb.get_posts('LibraryofObscureCopypastas',pages=4)
        self.posts_filtered = [[post["post_id"],post["text"],"{}/{}/{}".format(post["time"].strftime("%Y"),post["time"].strftime("%m"),post["time"].strftime("%d")),0] for post in posts_raw]
        self.new_posts_df = pd.DataFrame(self.posts_filtered, columns=self.headers).set_index("id")
        self.df_ids = self.df.index.values # get ids present
        self.new_ids = self.new_posts_df.index.values # new ids
        self.new_ids_exclude = [id for id in self.new_ids if id in self.df_ids] # get ids already present 
        self.new_posts_df = self.new_posts_df.drop(self.new_ids_exclude) # drop present ids
        self.df = self.df.append(self.new_posts_df) # append new posts to df
        self.df.to_csv(self.filename) # write updated df to file
    def newest_unused_pasta(self):
        """
        return newest unused pasta as string
        """
        self.read_df()
        ids = self.df.index[self.df['used'] == 0].tolist()
        try:
            self.latest_pasta = self.df.loc[ids[0],'pasta']
            self.df.loc[ids[0],'used'] = 1
        except:
            raise IndexError("All pasta used!")
        self.df.to_csv(self.filename)
        return self.latest_pasta
a = pasta_db(fn)
a.add_pasta()

print(a.df)
#pprint.pprint(a.posts_filtered)