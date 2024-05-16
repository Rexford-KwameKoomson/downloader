import customtkinter as ctk
import asyncio
from async_tkinter_loop import async_handler, async_mainloop
from tkinter import ttk
from pytube import YouTube
import os

# creating a function to trigger the download button
@async_handler
async def download_video():
    url = entry_url.get()
    print(url)

    resolutions = resolution_var.get()
    status_label.pack(pady=(10, 5))
    progress_label.pack(pady=(10, 5))
    progress_bar.pack(pady=(10, 5))

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.filter(res=resolutions).first()

        # Download the video into a specific directory
        output_path = os.path.join("downloads", f"{yt.title}.mp4")
        await asyncio.get_event_loop().run_in_executor(None, stream.download, output_path)
        status_label.configure(text="downloaded", text_color="White", fg_color="green")

    except Exception as k:
        status_label.configure(text=f"Error: {str(k)}", text_color="White", fg_color="red")


# creating the call back function for the on_progress
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completed = (bytes_downloaded / total_size) * 100

    progress_label.configure(text=str(int(percentage_completed)) + "%")
    progress_label.update()

    progress_bar.set(float(percentage_completed / 100))


# creating a root window
root = ctk.CTk()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

# Creating the title of the window
root.title("TA_Downloader")

# Set min and max width and height
root.geometry("720x480")
root.minsize(720, 480)
root.maxsize(1080, 720)

# creating a frame to hold the content
content_frame = ctk.CTkFrame(root)
content_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

# creating label and the entry widget for the video url
label = ctk.CTkLabel(content_frame, text="Enter the youtube link here: ")
entry_url = ctk.CTkEntry(content_frame, width=400, height=40)
label.pack(pady=(10, 5))
entry_url.pack(pady=(10, 5))

# Creating download button
download_button = ctk.CTkButton(content_frame, text="Download!", command=download_video)
download_button.pack(pady=(10, 5))

# Creating a list box/resolution box
resolutions = ("720px", "360px", "240px")
resolution_var = ctk.StringVar()
resolution_combobox = ttk.Combobox(content_frame, values=resolutions, textvariable=resolution_var)
resolution_combobox.pack(pady=(10, 5))
resolution_combobox.set("720px")

# creating a label and the progress bar to display the download progress
progress_label = ctk.CTkLabel(content_frame, text="0%")
progress_label.pack(pady=(10, 5))

progress_bar = ctk.CTkProgressBar(content_frame, width=400)
progress_bar.set(0)

# creating the status label
status_label = ctk.CTkLabel(content_frame, text="")

# to start the app
# async_mainloop(root)
root.mainloop()

