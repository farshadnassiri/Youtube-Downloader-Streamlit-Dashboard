import argparse

from pytubefix import YouTube
from tqdm import tqdm
from pytubefix.exceptions import VideoUnavailable


class YouTubeDownloader:
    def __init__(self,url,quality="highest",output_path="."):
        self.quality=quality
        self.url=url
        self.output_path=output_path
        self.yt=YouTube(self.url,
            on_progress_callback=self.on_progress,
            on_complete_callback=self.on_complete,
        )

        self.pbar=None

    def download(self):
        try:
            if self.quality=="highest":
                video_stream = self.yt.streams.filter(progressive=True,file_extension="mp4").get_highest_resolution()
            else:
                video_stream=self.yt.streams.filter(progressive=True,res=self.quality,file_extension="mp4").first()
            if video_stream is None:
                available_qualities=[ str(stream.resolution) for stream in self.yt.streams.filter(
                    progressive=True, file_extension="mp4")
                ]

                print(f"Title: {self.yt.title}")
                print(f"No video stream found for the given quality. Available qualities: {available_qualities}")
                return
    
            self.pbar=tqdm(total=video_stream.filesize,unit="B",unit_scale=True,desc="Downloading",leave=True)

            video_stream.download(output_path=self.output_path)
        except VideoUnavailable as e:
            print(f"Error downloading video: {e}")
            if self.pbar:
                self.pbar.close()

    def on_progress(self,stream,chunk,bytes_remaining):
        current=stream.filesize-bytes_remaining
        self.pbar.update(current-self.pbar.n)  

    def on_complete(self, stream, file_path):
        self.pbar.close()     
        print(f"\nDownloaded '{self.yt.title}' successfully to: {file_path}") 

def main():
    parser=argparse.ArgumentParser(description="Download a YouTube video at a specified quality and output path.") 

    parser.add_argument("url",help="The YouTube URL to download") 
    parser.add_argument("-q"
    ,"--quality",
    help="The desired video quality (e.g., 720p, 1080p, highest)",
    default="highest",
    type=str
    )
    parser.add_argument("-o",
        "--output_path",
        help="The output directory to save the video",
        default=".",
        type=str
    )    

    args=parser.parse_args()

    downloader=YouTubeDownloader(args.url,args.quality,args.output_path)
    downloader.download()

if __name__ == "__main__":
    main()



