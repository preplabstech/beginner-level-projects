#Youtube downloader using pytube

from email.charset import add_codec
from time import strftime,gmtime
from pytube import YouTube
import os
import ffmpeg
import re

class Yt_download():
    '''containing class of functions to fetch data and download the video'''

    def __init__(self,video):
        self.title = video.title
        self.len = video.length
        self.views = video.views
        self.a_stream = video.streams.filter(adaptive=True,only_audio=True).order_by('abr').desc()
        self.v_stream = video.streams.filter(adaptive=True,only_video=True).order_by('resolution').desc()
        self.ch_audio = ''
        self.ch_video = ''

    def make_choice(self):
        ''' 
        function for letting user to choose between
        audio, picture-only and video files to download
        '''

        print('-'*100)
        while True:
            ch_1 = input("Press:- \nv: video-only\na: audio-only\nv+: video with sound\n\n")

            if ch_1=='v' or ch_1=='V':

                # iterating over the list of video stream objects 
                # and showing data(resolution,file type,codec) about the video
                for i,entries in enumerate(self.v_stream):
                    print(f'{i+1}. type:{str(entries.mime_type)}  res:{entries.resolution!r}  fps:{entries.fps!r}')

                # assigning the selected video stream by the user
                self.ch_video = self.v_stream[int(input("select file: "))-1]
                break

            elif ch_1=='a' or ch_1=='A':

                # iterating over the list of audio stream objects 
                # and showing data(resolution,file type,codec) about the video
                for i,entries in enumerate(self.a_stream):
                    print(f'{i+1}. type:{str(entries.mime_type)}  abr:{entries.abr!r}  audio_codec:{entries.codecs!r}')
                
                #assigning the selected audio stream by the user
                self.ch_audio = self.a_stream[int(input("select file: "))-1]
                break

            elif ch_1=='v+' or ch_1=='V+':

                for i,entries in enumerate(self.v_stream):
                    print(f'{i+1}. type:{str(entries.mime_type)}  res:{entries.resolution!r}  fps:{entries.fps!r}')
                ch1 = int(input("\nselect video file: "))
                self.ch_video = self.v_stream[ch1-1]

                print("\n\n")

                for i,entries in enumerate(self.a_stream):
                    print(f'{i+1}. type:{str(entries.mime_type)}  abr:{entries.abr!r}  audio_codec:{entries.codecs!r}')
                ch2 = int(input("select audio file: "))
                self.ch_audio = self.a_stream[ch2-1]
                break

            else:
                # letting the user to make selection again
                #incase the user hits wrong input
                print('Invalid Input!\nTry Again\n\n')
                continue     
        
        # calling download() since user have already made their choise
        self.download()

    def show_info(self):
        '''
        function to display data(video title,total length) 
        of the video before doing the download
        '''
        #Title of the video
        print("Title: ",self.title,'\n')

        # converting the length of the video in seconds (returned by video.length)
        # into h:m:s easily readable format
        print("Duration: ",strftime("%Hh %Mm %Ss",gmtime(self.len)),'\n')

        #Number of views of video
        print("Number of views: ",self.views)
    
    def download(self):
        '''
        function to actually download, combine the video and audio
        files and save them inside pytube_Downloads/ folder.
        '''
        # removing special charecters from file name
        #  which cannot be used as filenames in windows
        name = re.sub("[|\/?*:;<>\".,]","",self.title)
        
        print("\nDownloading . . .\n")
        
        # only audio format is asked by the user
        if self.ch_audio and not self.ch_video:
            audio_fname = f'{name}-{self.ch_audio.abr}.mp3'
            if not os.path.exists(f'pytube_Downloads/{audio_fname}'):
                print('downloading mp3...\n')
                out_path = self.ch_audio.download(output_path='pytube_Downloads/')

                # renaming the downloaded audio file with bitrate tag
                new_name = os.path.splitext(out_path)
                os.rename(out_path,new_name[0] + f'-{self.ch_audio.abr}.mp3')
            else:
                print('file exists! skipping download')

        # only video format is asked by the user        
        elif self.ch_video and not self.ch_audio:
            video_fname = f'{name}-{self.ch_video.resolution}.mp4'
            
            if not os.path.exists(f'pytube_Downloads/{video_fname}'):
                print('downloading mp4...\n')
                out_path = self.ch_video.download(output_path='pytube_Downloads/')

                # renaming the downloaded video file with resolution tag
                new_name = os.path.splitext(out_path)
                os.rename(out_path,new_name[0] + f'-{self.ch_video.resolution}.mp4')
            else:
                print('file exists! skipping download')

        else:
        # download both the audio and video according to user's choise

            video_fname = f'{name}-{self.ch_video.resolution}.mp4'
            audio_fname = f'{name}-{self.ch_audio.abr}.mp3'
            print('downloading audio...')

            if not os.path.exists(f'pytube_Downloads/{audio_fname}'):
                out_path = self.ch_audio.download(output_path='pytube_Downloads/')
                new_name = os.path.splitext(out_path)
                os.rename(out_path,new_name[0] + f'-{self.ch_audio.abr}.mp3')

            else:
                print('file exists! skipping download')

            print('\ndownloading video...')

            if not os.path.exists(f'pytube_Downloads/{video_fname}'):
                out_path = self.ch_video.download(output_path='pytube_Downloads/')
                new_name = os.path.splitext(out_path)
                os.rename(out_path,new_name[0] + f'-{self.ch_video.resolution}.mp4')
            else:
               print('file exists! skipping download')

            print('\nCombining audio & video files using ffmpeg..')

            # ffmpeg-python is used here to recombine the seperate audio and video files
            # ffmpeg is not required to be installed on the system 
            # input files are passed to ffmpeg executable(.exe) 
            # ffmpeg.exe must be in the same folder as the program
            # setting vcodec=copy flag does not reencodes the video for faster processing
            audio_input = ffmpeg.input(f'pytube_Downloads/{audio_fname}')
            video_input = ffmpeg.input(f'pytube_Downloads/{video_fname}')
            out_stream = ffmpeg.output(video_input,audio_input,f'{name}-out.mp4',vcodec='copy')
            out_stream.run(overwrite_output=True, cmd='ffmpeg.exe',quiet=True)
        print("\nDone!\n")

yt_link = input("Enter the youtube video link: ")
video = YouTube(yt_link)
yt = Yt_download(video)
yt.show_info()
yt.make_choice()