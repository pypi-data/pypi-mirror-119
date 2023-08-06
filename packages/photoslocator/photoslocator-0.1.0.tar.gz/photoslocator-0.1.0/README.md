# photos_locator

<img align="right" width="30%" src="https://user-images.githubusercontent.com/50317336/132679652-9a2bcfec-9535-4e89-b720-afd5ee190eeb.png">
<div style="text-align: left"> 
<b>photos_locator</b> is a simple tool to rename your photos using datetime and gps metadata. Given a folder, it scrolls through all the photos and if they contain GPS metadata it renames them using the datetime and position in which they were taken. In detail:
<ul>
  <li>If the photo contains date and time of shooting and place, rename it in <b>YYYY-MM-DDThh:mm:ss-location</b></li>
  <li>If the photo contains only the date, rename it to <b>YYYY-MM-DDThh:mm:ss-original name</b></li>
  <li>If the photo does not contain the date, do not rename it </li>
</ul>  
</div>

## Installation

Run:

```bash
$ pip install photoslocator
```

to install application with pip. If you want to install photos_locator from sources, after you have downloaded it,
position yourself in the project root and install requirments using:

```bash
$ pip3 install -r requirements.txt
```

## Usage

```bash
$ photoslocator <path_to_photos_directory>
```