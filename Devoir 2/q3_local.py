import re
import os
import pandas as pd
from tqdm import tqdm
from q2_local import download_audio, cut_audio
from typing import List


def filter_df(csv_path: str, label: str) -> pd.DataFrame:
    """
    Write a function that takes the path to the processed csv from q1 (in the notebook) and returns a df of only the rows 
    that contain the human readable label passed as argument

    For example:
    get_ids("audio_segments_clean.csv", "Speech")
    """

    df_labels = pd.read_csv(csv_path)

    filtered_df = df_labels[df_labels['label_names'].apply(lambda x: label in x.split("|"))]
    
    return filtered_df
    


def data_pipeline(csv_path: str, label: str) -> None:
    """
    Using your previously created functions, write a function that takes a processed csv and for each video with the given label:
    (don't forget to create the audio/ folder and the associated label folder!). 
    1. Downloads it to <label>_raw/<ID>.mp3
    2. Cuts it to the appropriate segment
    3. Stores it in <label>_cut/<ID>.mp3

    It is recommended to iterate over the rows of filter_df().
    Use tqdm to track the progress of the download process (https://tqdm.github.io/)

    Unfortunately, it is possible that some of the videos cannot be downloaded. In such cases, your pipeline should handle the failure by going to the next video with the label.
    """

    filtered_df = filter_df(csv_path, label)
    
    os.makedirs("./audio/", exist_ok=True)
    raw_dir = "./audio/" + label + "_raw/"
    cut_dir = "./audio/" + label + "_cut/"
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(cut_dir, exist_ok=True)

    for _, row in tqdm(filtered_df.iterrows()):
        id = row["# YTID"]
        start = row[" start_seconds"]
        end = row[" end_seconds"]
        diff = int(end - start)

        in_path = raw_dir + id
        out_path = cut_dir + id + ".mp3"
        
        try:
            download_audio(id, in_path)
            if os.path.exists(in_path + ".mp3"):
                new_in_path = in_path + ".mp3"
                cut_audio(new_in_path, out_path, start, end)
        except Exception:
            continue


def rename_files(path_cut: str, csv_path: str) -> None:
    """
    Suppose we now want to rename the files we've downloaded in `path_cut` to include the start and end times as well as length of the segment. While
    this could have been done in the data_pipeline() function, suppose we forgot and don't want to download everything again.

    Write a function that, using regex (i.e. the `re` library), renames the existing files from "<ID>.mp3" -> "<ID>_<start_seconds_int>_<end_seconds_int>_<length_int>.mp3"
    in path_cut. csv_path is the path to the processed csv from q1. `path_cut` is a path to the folder with the cut audio.

    For example
    "--BfvyPmVMo.mp3" -> "--BfvyPmVMo_20_30_10.mp3"

    ## BE WARY: Assume that the YTID can contain special characters such as '.' or even '.mp3' ##
    """
    
    df = pd.read_csv(csv_path)

    if os.path.exists(path_cut):
        for filename in os.listdir(path_cut):
            is_matching = re.search(r"(.+)\.mp3", filename)

            if is_matching:
                ytid = is_matching.group(1)

                start = int(df.loc[df["# YTID"] == ytid][" start_seconds"].iloc[0])
                end = int(df.loc[df["# YTID"] == ytid][" end_seconds"].iloc[0])
                length = end - start

                new_filename = f"{ytid}_{start}_{end}_{length}.mp3"
            
                old_filepath = os.path.join(path_cut, filename)
                new_filepath = os.path.join(path_cut, new_filename)

                os.rename(old_filepath, new_filepath)


if __name__ == "__main__":
    print(filter_df("audio_segments_clean.csv", "Laughter"))
    data_pipeline("audio_segments_clean.csv", "Laughter")
    rename_files("Laughter_cut", "audio_segments_clean.csv")
