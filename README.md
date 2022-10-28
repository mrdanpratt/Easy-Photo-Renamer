# Easy Photo Renamer 0.1.0

## About the App

This app makes it easy to rename individual photos or entire groups of photos. This app will standardize the timestamp format (by extracting metadata) and add the (optional) description of your choice at the end of the filename. Alternatively, you can use only a description. Original files may be kept or discarded. If a file with the same name exists, the app will add a number within parentheses at the end of the new file's name. This is particularly useful when working with burst shots that have the same timestamp. Other functions include adding or removing arbitrary strings to and from photo filenames.

This app is the author's first attempt to create a fully-functional GUI app.

## Browse File(s)

Click the "File(s)" button to select one or more files in a folder for renaming. This app can rename the following file types: jpg, jpeg, png

## Browse Folder

Click the "Folder" button to select all the photos in a folder for renaming. This app can rename the following file types: jpg, jpeg, png

## Destination Folder

Click the "Destination Folder" button to find a folder to which renamed photos will be copied. It can be the same folder as the Source Folder.

## Original File:

Select "Discard" if you only want to keep the renamed photo(s). Select "Keep" if you would like to preserve the original photo(s).

## Rename Photo Using...

Select the first option if you would like to rename your photo with the timestamp followed by the (optional) description of your choice. Select the second option if you would like to rename your photo only with the description of your choice. Choosing the latter will disable the options below it.

## Use Dropdowns To Choose Separators for Exif Timestamp Formatting

You can individually choose between several characters to go in between the various parts of the timestamp. Options include a period, hyphen, underscore, space, or nothing at all.

## If No Exif Timestamp Exists, Rename Photo Using...

In case your photo contains no timestamp metadata, this selection will determine what happens. Select the first option to make no changes. Select the second option to preserve the original name followed by the (optional) description of your choice. Select the third option to discard the original name and rename the photo with only the description.

## Directional Buttons

Use these buttons to toggle through the photos in the Source you selected. If you elect to discard the original photo files, they will no longer be available to view after renaming.

## Enter Photo Description

Use the entry field to enter the description of your choice to use in renaming your photos. The app will automatically insert a space between the timestamp and the description. If the field is blank and you elected to use a timestamp, the photo will be renamed with the timestamp only. After every renaming event, the text in the entry field will be deleted.

## Rename Photo

Click the "Rename Photo" button (Return key) to rename the photo. After every photo renaming, the next photo in the Source will display and be ready for renaming.

## Batch Rename All

Click the "Batch Rename All" button to rename all the photos in your selection according to the present settings. If you have already renamed any photos and discarded originals, you will be prompted to make a new selection of photos.

## Add String to Photo Name(s)

This functionality is found under the Advanced menu. Browse for files or folders, enter the exact characters to add to the filename(s), adjust settings, and click the "Add String to Photo Name(s)" button to add the string to the names of the relevant photos (at the end, beginning, or after n characters).

## Remove String from Photo Name(s)

This functionality is found under the Advanced menu. Browse for files or folders, enter the exact characters to remove from the filename(s), adjust settings, and click the "Remove String from Photo Name(s)" button to remove the nth occurrence of the string (from the beginning or end of the filename) from the names of the relevant photos.

## License

Copyright © 2022 Dan Pratt

This project is licensed under the terms of the MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.