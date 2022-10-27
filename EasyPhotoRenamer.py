software_version = 'Easy Photo Renamer 0.1.0'

from tkinter import *
from tkinter import filedialog, messagebox, Menu

from PIL import ImageTk, Image, ImageOps

from glob import glob

from shutil import copy

from os import remove, rename, path

from os.path import exists

from sys import platform

# for Browse Source Folder shortcut
# calls browse_source
def browse_source_shortcut(event):
    browse_source()

# button activated by browse_source_btn
# calls list_pics, check_for_pics, start_count, limit_count, open_pic, down_up_btn_state, show_default
# finds the folder from which to copy and rename photos
def browse_source():
    global source_path
    global user_dir
    
    source_path = filedialog.askdirectory(initialdir = user_dir, title = 'Browse Folder')
    
    # when user selects a folder
    if source_path != None and source_path != '':
        
        # display source folder in text label
        source_lbl.config(text = short_path(source_path))
        list_pics()
        check_for_pics()
        
        # if there are actually photos in the source folder
        if yes_pics == True:
            user_dir = source_path
            start_count()
            limit_count()
            number_of_pics.config(text = f'{len(main_pic_list)} Photos Selected')
            direction = 'up'
            open_pic(direction)
            down_up_btn_state(yes_pics)
            window.focus_force()
        
        # if there are no photos in the source folder
        else:
            show_default()
            number_of_pics.config(text = '')
            down_up_btn_state(yes_pics)
            window.focus_force()
    
    # in case user doesn't select a folder or selects nothing
    elif source_path == '':
        show_default()
        number_of_pics.config(text = '')
        source_lbl.config(text = 'No Source Selected')
        window.focus_force()
    
    # if source folder is somehow null
    else:
        show_default()
        number_of_pics.config(text = '')
        window.focus_force()

# for Browse Specific File(s) shortcut
# calls browse_speci_files
def browse_speci_files_shortcut(event):
    browse_speci_files()

# activated by Advanced->Browse Specific File(s) menu option
# similar to browse_source function
# calls speci_list_pics, check_for_pics, start_count, limit_count, open_pic, down_up_btn_state, and show_default
def browse_speci_files():
    global speci_files
    global source_path
    global user_dir

    speci_files = filedialog.askopenfilenames(initialdir = user_dir, title = 'Browse File(s)')
    try:
        source_path = speci_files[0].rsplit('/', 1)[0]
    except:
        pass
    
    # when user selects a folder
    if speci_files != None and speci_files != '':
        
        # display source folder in text label
        source_lbl.config(text = short_path(source_path))
        speci_list_pics()
        check_for_pics()
        
        # if there are actually photos in the source
        if yes_pics == True:
            user_dir = source_path
            start_count()
            limit_count()
            number_of_pics.config(text = f'{len(main_pic_list)} Photos Selected')
            direction = 'up'
            open_pic(direction)
            down_up_btn_state(yes_pics)
            window.focus_force()
        
        # if there are no photos in the source
        else:
            show_default()
            number_of_pics.config(text = '')
            down_up_btn_state(yes_pics)
            window.focus_force()
    
    # in case user doesn't select a folder or selects nothing
    elif speci_files == '':
        show_default()
        number_of_pics.config(text = '')
        source_lbl.config(text = 'No Source Selected')
        window.focus_force()
    
    # if source is somehow null
    else:
        show_default()
        number_of_pics.config(text = '')
        window.focus_force()

# for Browse Destination Folder shortcut
# calls browse_dest
def browse_dest_shortcut(event):
    browse_dest()

# button activated by browse_dest_btn
# finds the folder to which newly-renamed photos will be copied
def browse_dest():
    global dest_path
    
    dest_path = filedialog.askdirectory(initialdir = user_dir, title = 'Destination Folder')
    
    # if user selects a valid destination folder
    if dest_path != None and dest_path != '':
        
        # display destination folder in text label
        # gets the user ready to input a photo description
        dest_lbl.config(text = short_path(dest_path))
        enter_new_name.focus()
    
    # if user selects nothing
    elif dest_path == '':
        dest_lbl.config(text = 'No Destination Folder Selected')
        window.focus_force()
    
    # if destination folder is somehow null
    else:
        window.focus_force()

# makes the source_path or dest_path end in elipsis if too long for label
def short_path(dir):
    if len(dir) <= 77:
        return dir
    else:
        return f'{dir[0:76]}...'

# called in browse_source function
# builds list of all jpg's, jpeg's, and png's and sorts them ascending
def list_pics():
    global main_pic_list
    
    main_pic_list = glob(source_path + '/*.jpg')
    main_pic_list.extend(glob(source_path + '/*.jpeg'))
    main_pic_list.extend(glob(source_path + '/*.png'))
    main_pic_list.sort()

# called by browse_speci_files
# similar to list_pics
def speci_list_pics():
    global speci_files
    global main_pic_list
    
    main_pic_list = []
    file_types = ['jpg', 'jpeg', 'png']
    for i in speci_files:
        if i.rsplit('.', 1)[1] in file_types:
            main_pic_list.append(i)
    main_pic_list.sort()

# called in browse_source, browse_speci_files, count_up, count_down
# calls open_image, show_no_further, show_no_previous, show_not_found
# parameter direction is either 'up' or 'down'
# accounts for file not existing anymore
def open_pic(direction):
    global count
    
    try:
        open_image()
    
    # if the image doesn't open (probably due to being deleted by app or by another process while app is working)
    except:
        if direction == 'up':
            
            # while photo doesn't exist, keeps trying the next photo in ascending order if not on last index of main_pic_list
            while exists(main_pic_list[count]) == False and count != max_count:
                count += 1
            
            # if photo doesn't exist and app is on last possible index of main_pic_list, calls show_no_further
            if exists(main_pic_list[count]) == False and count == max_count:
                show_no_further()
            
            # when photo does exist
            else:
                try:
                    open_image()
                except:
                    show_not_found()
        
        # if direction == 'down'
        else:
            
            # while photo doesn't exist, keeps trying the next photo in descending order if not on first index of main_pic_list
            while exists(main_pic_list[count]) == False and count != min_count:
                count -= 1
            
            # if photo doesn't exist and app is on first possible index of main_pic_list, calls show_no_previous
            if exists(main_pic_list[count]) == False and count == min_count:
                show_no_previous()
            
            # when photo does exist
            else:
                try:
                    open_image()
                except:
                    show_not_found()

# called in open_pic
# calls pic_namer
# opens image and orients correctly, reduces to max_size, configs pic_lbl
def open_image():
    img = ImageOps.exif_transpose(Image.open(main_pic_list[count]))
    img.thumbnail(max_size)
    img = ImageTk.PhotoImage(img)
    pic_lbl.config(image = img)
    pic_lbl.image = img
    pic_namer()

# called by browse_source and browse_speci_files
# for activating/deactivating left, right buttons
def down_up_btn_state(yes_pics):
    if yes_pics and len(main_pic_list) > 1:
        count_up_btn.config(state = 'active')
    else:
        count_down_btn.config(state = 'disabled')
        count_up_btn.config(state = 'disabled')

# called in browse_source function
# begins a count at zero for purpose of having an index to search list of photos
def start_count():
    global count
    count = 0

# called in browse_source function
# determines length of the list of photos and sets an appropriate min & max
def limit_count():
    global max_count
    
    max_count = len(main_pic_list) - 1
    global min_count
    min_count = 0

# called in browse_source function
# checks if there are jpg's, jpeg's, or png's in the source folder; if not, gives warning
# adjusts yes_pics to True or False
def check_for_pics():
    if len(main_pic_list) == 0:
        messagebox.showinfo('No Photos', 'Please Select a Source with a Photo')
        window.focus_force()
        global yes_pics
        yes_pics = False
    else:
        yes_pics = True

# called in browse_source function
# displays a default image in the image label, blanks out pic_name_lbl
def show_default():
    img = ImageOps.exif_transpose(Image.open('PicRenamerDefaultPic.png'))
    img.thumbnail(max_size)
    img = ImageTk.PhotoImage(img)
    pic_lbl.config(image = img)
    pic_lbl.image = img
    pic_name_lbl.config(text = '')

# called in open_pic
# default 'not found' image in case there is a problem opening up photo, blanks out pic_name_lbl
def show_not_found():
    img = ImageOps.exif_transpose(Image.open('PicRenamerPhotoNotFound.png'))
    img.thumbnail(max_size)
    img = ImageTk.PhotoImage(img)
    pic_lbl.config(image = img)
    pic_lbl.image = img
    pic_name_lbl.config(text = '')

# called in open_pic
# if the first photo in main_pic_list is missing and user navigates to beginning of list, blanks out pic_name_lbl
def show_no_previous():
    img = ImageOps.exif_transpose(Image.open('NoPreviousPhotos.png'))
    img.thumbnail(max_size)
    img = ImageTk.PhotoImage(img)
    pic_lbl.config(image = img)
    pic_lbl.image = img
    pic_name_lbl.config(text = '')

# called in open_pic
# if the last photo in main_pic_list is missing and user navigates to end of list, blanks out pic_name_lbl
def show_no_further():
    img = ImageOps.exif_transpose(Image.open('NoFurtherPhotos.png'))
    img.thumbnail(max_size)
    img = ImageTk.PhotoImage(img)
    pic_lbl.config(image = img)
    pic_lbl.image = img
    pic_name_lbl.config(text = '')

# called in open_image
# finds name of the photo and displays in pic_name_lbl
def pic_namer():
    global pic_name
    
    pic_name = main_pic_list[count].split(f'{source_path}/')[1]
    pic_name_lbl.config(text = pic_name)

# for previous photo shortcut
# calls count_down
def count_down_shortcut(event):
    count_down()

# button activated by count_down_btn
# decreases by one the index used by the list of photos for displaying and manipulationg purposes
# calls open_pic
def count_down():
    
    # checks various things to see if there is a legit source folder with photos
    if 'count' not in globals() or 'source_path' not in globals() or source_path == '' or yes_pics == False:
        pass
    else:
        global count
        
        # if on first photo and it has somehow been deleted or altered
        if count == min_count and exists(main_pic_list[count]) == False:
            show_no_previous()
        
        # if on last photo
        elif count == min_count:
            pass
        else:
            count -= 1
            direction = 'down'
            open_pic(direction)
            
            #activate & deactivate buttons depending on count
            if count <= max_count - 1:
                count_up_btn.config(state = 'active')
            if count == min_count:
                count_down_btn.config(state = 'disabled')
            
            # gets user ready to adjust photo description
            enter_new_name.select_range(0, END)

# for next photo shortcut
# calls count_up
def count_up_shortcut(event):
    count_up()

# button activated by count_up_btn
# increases by one the index used by the list of photos for displaying and manipulationg purposes
# calls show_no_further, open_pic
def count_up():
    
    # checks various things to see if there is a legit source folder with photos
    if 'count' not in globals() or 'source_path' not in globals() or source_path == '' or yes_pics ==  False:
        pass
    else:
        global count
        
        # if on last photo and it has somehow been deleted or altered
        if count == max_count and exists(main_pic_list[count]) == False:
            show_no_further()
        
        # if on last photo
        elif count == max_count:
            pass
        else:
            direction = 'up'
            count += 1
            open_pic(direction)
            
            #activate & deactivate buttons depending on count
            if count >= min_count + 1:
                count_down_btn.config(state = 'active')
            if count == max_count:
                count_up_btn.config(state = 'disabled')
            
            # gets user ready to adjust photo description
            enter_new_name.select_range(0, END)

# for rename photo shortcut
# calls copy_pic
def copy_pic_shortcut(event):
    copy_pic()

# called by copy_pic_shortcut and batch
# calls keep_or_discard, count_up
# renames and copies photo from source folder to destination folder
def copy_pic():
    
    # checks if legit source folder with photos has been selected
    if 'count' not in globals() or yes_pics == False:
        messagebox.showinfo('Error', 'Please Select a Source with a Photo')
        window.focus_force()
    
    #  checks if there is a destination folder
    elif 'dest_path' not in globals() or dest_path == '':
        messagebox.showinfo('Error', 'Please Select a Destination Folder')
        window.focus_force()
    
    # this might be extraneous
    elif 'source_path' not in globals() or source_path == '':
        messagebox.showinfo('Error', 'Please Select a Source with a Photo')
        window.focus_force()
    
    # if user has decided to forego renaming using a timestamp but has not entered a description
    elif time_stamp_var.get() == 'Description Only' and enter_new_name.get() == '':
        messagebox.showinfo('Error', 'Please Enter a Description')
        window.focus_force()
        enter_new_name.focus()
    
    # if timestamp & description selected and 2nd description only is selected, force a description entry
    elif time_stamp_var.get() == 'Timestamp & Description' and if_no_exif_var.get() == 'Description Only' and enter_new_name.get() == '':
        messagebox.showinfo('Error', 'Please Enter a Description in Case of No Exif Timestamp')
        window.focus_force()
        enter_new_name.focus()
    
    # if the current photo doesn't exist anymore
    elif exists(main_pic_list[count]) == False:
        messagebox.showinfo('Error', 'Photo Has Been Removed or Renamed')
        window.focus_force()
    
    # check for illegal characters
    elif any(i in enter_new_name.get() for i in illegal_characters):
            messagebox.showinfo('Error', illegal_characters_warning)
            window.focus_force()
            enter_new_name.focus()
    
    # first assumes there is Exif timestamp, tries getting it, and creates a photo_date based on it, including user-selected separators
    else:
        no_exif_timestamp = False
        
        # extract exif timestamp & change formatting depending on dropdown choices
        try:
            photo_date = Image.open(main_pic_list[count])._getexif()[36867]
            photo_date = photo_date.replace(':', options_dict[ym.get()], 1)
            photo_date = photo_date.replace(':', options_dict[md.get()], 1)
            photo_date = photo_date.replace(' ', options_dict[dh.get()], 1)
            photo_date = photo_date.replace(':', options_dict[hm.get()], 1)
            photo_date = photo_date.replace(':', options_dict[ms.get()], 1)
        
        # in case no exif timestamp, original name of file remains
        except:
            no_exif_timestamp = True
            photo_date = pic_name.rsplit('.', 1)[0]
        
        # creates var appendage based on user-provided description
        appendage = enter_new_name.get()
        
        # if no Exif timestamp and "original only" was selected, no change in name
        if time_stamp_var.get() == 'Timestamp & Description' and no_exif_timestamp == True and if_no_exif_var.get() == 'Original Name Only':
            new_name = pic_name
        
        # if user doesn't want timestamp in photo name
        elif time_stamp_var.get() == 'Description Only':
            
            # concat description & .filetype
            new_name = f'{appendage}.{pic_name.rsplit(".", 1)[1]}'
        
        # if there was no timesetamp and user chose to discard original name in such a situation
        elif no_exif_timestamp == True and if_no_exif_var.get() == 'Description Only':
            
            # concat description & .filetype
            new_name = f'{appendage}.{pic_name.rsplit(".", 1)[1]}'
        else:
            
            # if user hasn't written anything in description box
            if appendage == '':
                
                # concat date & .filetype
                new_name = f'{photo_date}.{pic_name.rsplit(".", 1)[1]}'
            else:
                
                # concat date & space & appendage & .filetype
                new_name = f'{photo_date} {appendage}.{pic_name.rsplit(".", 1)[1]}'
        
        # if working in one folder, discard set, and the name doesn't change; don't rename and count_up
        if source_path == dest_path and keep_var.get() == 'Discard' and pic_name == new_name:
            if count == max_count and batch_true != True:
                    messagebox.showinfo('Done', 'You have renamed the last photo in your selection')
                    window.focus_force()
            count_up()
            enter_new_name.select_range(0, END)
        
        # check to see if file already exists, if so, add increasing number at end
        else:
            temp_name = new_name
            counter = 1
            while exists(f'{dest_path}/{temp_name}') == True:
                temp_name = f'{new_name.rsplit(".",1)[0]}({counter}).{new_name.rsplit(".", 1)[1]}'
                counter += 1
            new_name = temp_name
            
            # to tell batch() to stop if there is an error
            global copy_error
            
            # try to copy photo with new name and subsequent processes
            
            # use rename if same folder and discard original
            if source_path == dest_path and keep_var.get() == 'Discard':
                rename(f'{source_path}/{pic_name}', f'{dest_path}/{new_name}')
                if count == max_count and batch_true != True:
                    messagebox.showinfo('Done', 'You have renamed the last photo in your selection')
                    window.focus_force()
                copy_error = False
                count_up()
            
            else:
                try:
                    copy(f'{source_path}/{pic_name}', f'{dest_path}/{new_name}')
                    keep_or_discard()
                    if count == max_count and batch_true != True:
                        messagebox.showinfo('Done', 'You have renamed the last photo in your selection')
                        window.focus_force()
                    copy_error = False
                    count_up()
                
                # if there is not permission to copy or put photo in destination folder
                except PermissionError:
                    messagebox.showinfo('Error', 'Permission Denied')
                    copy_error = True
                    window.focus_force()
                
                # if there is any other problem
                except:
                    messagebox.showinfo('Error', 'Error in Renaming/Copying File')
                    copy_error = True
                    window.focus_force()
            
            # gets user ready to adjust description
            if batch_true:
                pass
            else:
                enter_new_name.delete(0, END)
        
# called in copy_pic
# if user has elected to discard original photo, removes it
def keep_or_discard():
    if keep_var.get() == 'Discard':
        try:
            remove(main_pic_list[count])
            main_pic_list_exist = []
            for i in main_pic_list:
                main_pic_list_exist.append(exists(i))
            number_of_pics.config(text = f'{main_pic_list_exist.count(True)} Photos Selected')
        except:
            pass
    else:
        pass

# for batch rename shortcut
# calls batch
def batch_shortcut(event):
    batch()

# activated by Advanced->Batch Rename Entire Selection menu option
# starts with same checks as copy_pic to avoid large amount of messageboxes if checks fail during copy_pic
# calls copy_pic
def batch():
    global batch_true
    batch_true = True
    global count
    
    # to see if all the photos still exist
    main_pic_list_exist = []
    try:
        for i in main_pic_list:
            main_pic_list_exist.append(exists(i))
    except:
        pass
    
    # checks if legit source folder with photos has been selected
    if 'count' not in globals() or yes_pics == False:
        messagebox.showinfo('Error', 'Please Select a Source with a Photo')
        window.focus_force()
    
    #  checks if there is a destination folder
    elif 'dest_path' not in globals() or dest_path == '':
        messagebox.showinfo('Error', 'Please Select a Destination Folder')
        window.focus_force()
    
    # this might be extraneous
    elif 'source_path' not in globals() or source_path == '':
        messagebox.showinfo('Error', 'Please Select a Source with a Photo')
        window.focus_force()
    
    # if user has decided to forego renaming using a timestamp but has not entered a description
    elif time_stamp_var.get() == 'Description Only' and enter_new_name.get() == '':
        messagebox.showinfo('Error', 'Please Enter a Description')
        window.focus_force()
        enter_new_name.focus()
    
    # if timestamp & description selected and 2nd description only is selected, force a description entry
    elif time_stamp_var.get() == 'Timestamp & Description' and if_no_exif_var.get() == 'Description Only' and enter_new_name.get() == '':
        messagebox.showinfo('Error', 'Please Enter a Description in Case of No Exif Timestamp')
        window.focus_force()
        enter_new_name.focus()
    
    # if the current photo doesn't exist anymore
    elif exists(main_pic_list[count]) == False:
        messagebox.showinfo('Error', 'Photo Has Been Removed or Renamed')
        window.focus_force()
    
    # checks if any photos in selection have been removed or renamed already
    elif False in main_pic_list_exist:
        messagebox.showinfo('Error', 'Some of the photos in your selection have been removed or renamed. Please browse a new selection before batch renaming.')
        window.focus_force()
    
    # check for illegal characters
    elif any(i in enter_new_name.get() for i in illegal_characters):
            messagebox.showinfo('Error', illegal_characters_warning)
            window.focus_force()
            enter_new_name.focus()
    
    # first assumes there is Exif timestamp, tries getting it, and creates a photo_date based on it, including user-selected separators
    else:
        reply = messagebox.askokcancel('Warning', 'This will rename all photos in your entire selection according to the settings you have selected. If you are renaming many photos, it could take several minutes.')
        if reply == False:
            pass
        if reply == True:
            count = 0
            direction = 'down'
            open_pic(direction)
            global copy_error
            for i in main_pic_list:
                copy_pic()
                if copy_error:
                    break
            if copy_error:
                messagebox.showinfo('Error', 'Batch rename process interrupted - Photos have not been renamed')
            else:
                messagebox.showinfo('Complete', 'All photos in selection have been renamed')
            copy_error = False
            window.focus_force()
            enter_new_name.delete(0, END)

    batch_true = False

# activated when user selects either 'Timestamp & Description' or 'Description Only'
# either activates further options (and blackens further text) or disables further options (and grays out further text)
def timestamp_or_no():
    widgets_to_config = [
        date_format_lbl,
        year_lbl,
        year_month_dropdown,
        month_lbl,
        month_day_dropdown,
        day_lbl,
        day_hour_dropdown,
        hour_lbl,
        hour_min_dropdown,
        min_lbl,
        min_sec_dropdown,
        sec_lbl,
        if_no_exif_lbl,
        original_only,
        original_and_description,
        no_original_description_only
    ]
    
    if time_stamp_var.get() == 'Timestamp & Description':
        original_only.select()
        for i in widgets_to_config:
            i.config(state = 'active')
    if time_stamp_var.get() == 'Description Only':
        no_original_description_only.select()
        for i in widgets_to_config:
            i.config(state = 'disabled')

# Changes 'Cmd' to 'Ctrl' and 'Command' to 'Control' for non-Mac os
def os_appropriate_command(key_combo):
    if platform == 'darwin':
        return key_combo
    else:
        if key_combo[0] == '<':
            return f'<Control{key_combo.split("<Command", 1)[1]}'
        else:
            return f'Ctrl{key_combo.split("Cmd", 1)[1]}'

# for keyboard shortcut
def append_window_shortcut(event):
    check_for_append_window()

# for keyboard shortcut
def close_append_window_shortcut(event):
    append_window.destroy()

# checks if append_window already open
def check_for_append_window():
    global append_window
    if append_window:
        try:
            append_window.focus_force()
        except:
            start_append_window()
    else:
        start_append_window()

# special functionalisty 'add string to photo name'
def start_append_window():
    global append_window
    global append_pic_list
    append_pic_list = []

    # for keyboard shortcut
    def append_browse_file_shortcut(event):
        append_browse_file()
    
    # browse specific files
    def append_browse_file():
        global user_dir
        global append_source
        append_source = None
        
        append_files = filedialog.askopenfilenames(initialdir = user_dir, title = 'Browse File(s)')
        
        # to get the directory without a file attached
        try:
            append_source = append_files[0].rsplit('/', 1)[0]
        except:
            pass
        
        # if user cancels or somehow selects nothing
        if append_source == None or append_source == '':
            append_no_of_selected_photos.config(text = '')
            append_source_label.config(text = 'No Source Selected')
            messagebox.showinfo('No Photos', 'Please Select a Source with a Photo')
            append_window.focus_force()
            append_entry.select_range(0, END)
        
        # if there is a legit source
        elif append_source != None and append_source != '':
            
            # display source folder in text label
            append_source_label.config(text = short_path(append_source))
            
            # build list of photos and sort
            global append_pic_list
            append_pic_list = []
            file_types = ['jpg', 'jpeg', 'png']
            for i in append_files:
                if i.rsplit('.', 1)[1] in file_types:
                    append_pic_list.append(i)
            append_pic_list.sort()
            
            # display number of photos selected
            append_no_of_selected_photos.config(text = f'{len(append_pic_list)} Photos Selected')
            
            # if no actual photos in list
            if len(append_pic_list) == 0:
                append_no_of_selected_photos.config(text = '')
                messagebox.showinfo('No Photos', 'Please Select a Source with a Photo')
            
            # if there are photos in list
            else:
                user_dir = append_source
            append_window.focus_force()
            append_entry.focus()
        
        # if source folder is somehow null
        else:
            append_no_of_selected_photos.config(text = '')
            append_source_label.config(text = 'No Source Selected')
            append_window.focus_force()
            append_entry.select_range(0, END)

    # for keyboard shortcut
    def append_browse_folder_shortcut(event):
        append_browse_folder()
    
    # browse entire folder
    def append_browse_folder():
        global user_dir
        global append_source
        append_source = None
        
        append_source = filedialog.askdirectory(initialdir = user_dir, title = 'Browse Folder')
        
        # if user cancels or somehow selects nothing
        if append_source == None or append_source == '':
            append_no_of_selected_photos.config(text = '')
            append_source_label.config(text = 'No Source Selected')
            messagebox.showinfo('No Photos', 'Please Select a Source with a Photo')
            append_window.focus_force()
            append_entry.select_range(0, END)
        
        # if the user selects a source
        elif append_source != None and append_source != '':
            
            # display source folder in text label
            append_source_label.config(text = short_path(append_source))
            
            # build and sort list of photos
            global append_pic_list
            append_pic_list = []
            append_pic_list = glob(append_source + '/*.jpg')
            append_pic_list.extend(glob(append_source + '/*.jpeg'))
            append_pic_list.extend(glob(append_source + '/*.png'))
            append_pic_list.sort()
            
            # change label for number of photos selected
            append_no_of_selected_photos.config(text = f'{len(append_pic_list)} Photos Selected')
            
            # if there are no photos
            if len(append_pic_list) == 0:
                append_no_of_selected_photos.config(text = '')
                messagebox.showinfo('No Photos', 'Please Select a Source with a Photo')
            
            # if there are photos
            else:
                user_dir = append_source
            append_window.focus_force()
            append_entry.focus()
        
        # if source folder is somehow null
        else:
            append_no_of_selected_photos.config(text = '')
            append_window.focus_force()
            append_entry.select_range(0, END)

    # keyboard shortcut
    def append_shortcut(event):
        append()
    
    # button (or shortcut) activated
    # adds string (from entry) to end, beginning, or after n characters
    def append():
        global append_pic_list
        
        # if there are no photos
        if append_pic_list == [] or len(append_pic_list) == 0:
            messagebox.showinfo('No Photos', 'Please Select a Source with a Photo')
            append_window.focus_force()
            append_entry.select_range(0, END)
        
        # if nothing in entry box
        elif append_entry.get() == '':
            messagebox.showinfo('No Entry', 'Please enter something to append')
            append_window.focus_force()
            append_entry.select_range(0, END)
        
        # if entry box contains illegal characters
        elif any(i in append_entry.get() for i in illegal_characters):
            messagebox.showinfo('Error', illegal_characters_warning)
            append_window.focus_force()
            append_entry.select_range(0, END)
        
        # if user has selected add string after n characters and if the number of characters is a non-negative integer
        elif append_end_beg_mid_var.get() == 'middle' and entry_is_non_neg_int(append_after_characters_entry.get()) == False:
            messagebox.showinfo('Error', 'Please enter a non-negative integer with no decimals in the "Add String After x Characters" entry box (e.g. "1", "2", etc).')
            append_window.focus_force()
        
        # process to adjust list of photos to fit user settings
        else:
            append_pic_list_adjusted = []
            
            # if user selects to add string after n characters
            if append_end_beg_mid_var.get() == 'middle':
                
                # entry of number of characters assured to be int
                # make string int n
                n = int(append_after_characters_entry.get())
                
                for i in append_pic_list:
                    
                    # gets file without directory
                    file = i.rsplit('/', 1)[1]
                    
                    # gets file without extension
                    file_without_ext = file.rsplit('.', 1)[0]
                    
                    # if length of filename at least as long as n, add to adjusted list
                    if len(file_without_ext) >= n:
                        append_pic_list_adjusted.append(i)
            
            # if user selects to add string to end or beginning
            else:
                
                # adjusted list same as first list
                append_pic_list_adjusted = append_pic_list
                n = 0
            
            # if adjusted list has no photos
            if len(append_pic_list_adjusted) == 0:
                messagebox.showinfo('Error', f'According to your settings,\nthere are no photos to which to add the string:\n"{append_entry.get()}"')
                append_window.focus_force()
            
            # if adjusted list has photos
            else:
                
                # warn user of what will happen
                reply = messagebox.askokcancel('Warning', f'This will add the string:\n"{append_entry.get()}"\n{append_warning_message(append_end_beg_mid_var.get(), n)} {len(append_pic_list_adjusted)} photo name(s)')
                
                # if user cancels
                if reply == False:
                    append_window.focus_force()
                    append_entry.select_range(0, END)
                
                # if user proceeds
                else:
                    for i in append_pic_list_adjusted:
                        
                        # split each photo into constituent parts
                        directory_stub = i.rsplit('/', 1)[0]
                        file_name_with_ext = i.rsplit('/', 1)[1]
                        file_name_without_ext = file_name_with_ext.rsplit('.', 1)[0]
                        file_ext = i.rsplit('.', 1)[1]
                        
                        # get string to add from entry
                        new_string = append_entry.get()
                        
                        # if user wants to add string to end
                        if append_end_beg_mid_var.get() == 'end':
                            new_name = f'{directory_stub}/{file_name_without_ext}{new_string}.{file_ext}'
                        
                        # if user wants to add string after n characters or at beginning (after 0 characters)
                        else:
                            
                            # new file name without extension = the first n characters + string to add + rest of the characters
                            new_file_name = file_name_without_ext[:n] + new_string + file_name_without_ext[n:]
                            
                            # put it together with directory and extension
                            new_name = f'{directory_stub}/{new_file_name}.{file_ext}'
                        
                        # process to add (#) to duplicate files to prevent collision of filenames
                        
                        # make a temporary name
                        temp_name = new_name
                        
                        # start a counter
                        counter = 1
                        
                        # if file already exists
                        while exists(temp_name) == True:
                            
                            # temp name becomes new name without ext + (#) + .file extension
                            temp_name = f'{new_name.rsplit(".", 1)[0]}({counter}).{new_name.rsplit(".", 1)[1]}'
                            
                            # counter goes up by 1
                            counter += 1
                        
                        # once an iteration of the filename does not already exist, assign temp name to new name
                        new_name = temp_name
                        
                        # rename photo with new name
                        rename(i, new_name)
                    
                    # cleanup and reset after process is complete
                    append_pic_list = []
                    append_no_of_selected_photos.config(text = '')
                    append_source_label.config(text = 'No Source Selected')
                    messagebox.showinfo('Process Complete', 'The strings have been added to the names of your photos')
                    illegal_entry = False
                    append_window.focus_force()
                    append_entry.delete(0, END)
                    append_to_end_btn.select()
                    append_after_characters_entry.delete(0, END)
                    append_entry.focus()
        
    # determine if string is a non-negative integer
    def entry_is_non_neg_int(entry):
        try:
            n = int(entry)
            if n >= 0:
                return True
            else:
                return False
        except:
            return False

    # changes warning message based on user settings
    def append_warning_message(option, n):
        if option == 'middle':
            return f'after {n} characters for'
        else:
            return f'to the {option} of'

    # tkinter window of 'add string to phot name' functionality
    append_window = Toplevel(window)
    append_window.geometry('700x250')
    append_window.title('Add String to Photo Name(s)')

    append_menubar = Menu(append_window)
    append_window.config(menu = append_menubar)
    append_menu = Menu(append_menubar, tearoff = 0)
    append_menu.add_command(label = 'Open File(s)...', command = append_browse_file, accelerator = os_appropriate_command('Cmd-O'))
    append_menu.add_command(label = 'Open Folder...', command = append_browse_folder, accelerator = os_appropriate_command('Cmd-Shift-O'))
    append_menu.add_command(label = 'Append Photo Name(s)', command = append, accelerator = 'Return')
    append_menu.add_command(label = 'Close Append Window', command = append_window.destroy, accelerator = os_appropriate_command('Cmd-W'))
    append_menubar.add_cascade(label = 'Add String', menu = append_menu)
    append_window.bind(os_appropriate_command('<Command-o>'), append_browse_file_shortcut)
    append_window.bind(os_appropriate_command('<Command-Shift-O>'), append_browse_folder_shortcut)
    append_window.bind(os_appropriate_command('<Return>'), append_shortcut)
    append_window.bind(os_appropriate_command('<Command-w>'), close_append_window_shortcut)

    append_browse_label = Label(append_window, text = 'Browse...')
    append_no_of_selected_photos = Label(append_window, text = '')
    append_browse_files_btn = Button(append_window, text = 'Files(s)', command = append_browse_file)
    append_browse_folder_btn = Button(append_window, text = 'Folder', command = append_browse_folder)
    append_source_label = Label(append_window, text = 'No Source Selected', anchor = 'w')
    append_entry_label = Label(append_window, text = 'Enter the exact characters to add to photo name(s)')
    append_entry = Entry(append_window)
    append_entry.focus()
    append_end_beg_mid_var = StringVar(value = 'end')
    append_to_end_btn = Radiobutton(append_window, text = 'Add String to End', variable = append_end_beg_mid_var, value = 'end')
    append_to_beg_btn = Radiobutton(append_window, text = 'Add String to Beginning', variable = append_end_beg_mid_var, value = 'beginning')
    append_to_mid_btn = Radiobutton(append_window, text = 'Add String After', variable = append_end_beg_mid_var, value = 'middle')
    append_after_characters_entry = Entry(append_window)
    append_after_characters_label = Label(append_window, text = 'Characters (enter a positive integer)')
    append_button = Button(append_window, text = 'Add String to Photo Name(s)', default = 'active', command = append)

    append_browse_label.place(x = 30, y = 20)
    append_no_of_selected_photos.place(x = 170, y = 20)
    append_browse_files_btn.place(x = 30, y = 40, width = 70)
    append_browse_folder_btn.place(x = 100, y =40, width = 70)
    append_source_label.place(x = 170, y = 45, width = 530)
    append_entry_label.place(x = 30, y = 70)
    append_entry.place(x = 30, y = 95, width = 200)
    append_to_end_btn.place(x = 30, y = 125)
    append_to_beg_btn.place(x = 30, y = 150)
    append_to_mid_btn.place(x = 30, y = 175)
    append_after_characters_entry.place(x = 155, y = 175, width = 30)
    append_after_characters_label.place(x = 185, y = 175)
    append_button.place(x = 30, y = 205, width = 200)

    append_window.mainloop()

# for keyboard shortcut
def remove_string_window_shortcut(event):
    check_for_remove_string_window()

# for keyboard shortcut
def close_remove_string_window_shortcut(event):
    remove_string_window.destroy()

# checks to see if remove string window already open
def check_for_remove_string_window():
    global remove_string_window
    if remove_string_window:
        try:
            remove_string_window.focus_force()
        except:
            start_remove_string_window()
    else:
        start_remove_string_window()

# special functionalisty 'remove string from photo name'
def start_remove_string_window():
    global remove_string_window
    global remove_string_pic_list
    remove_string_pic_list = []

    # for keyboard shortcut
    def remove_string_browse_file_shortcut(event):
        remove_string_browse_file()
    
    # browse specific files
    def remove_string_browse_file():
        global user_dir
        global remove_string_source
        remove_string_source = None
        
        remove_string_files = filedialog.askopenfilenames(initialdir = user_dir, title = 'Browse File(s)')
        
        # to get the directory without a file attached
        try:
            remove_string_source = remove_string_files[0].rsplit('/', 1)[0]
        except:
            pass
        
        # if user cancels or somehow selects nothing
        if remove_string_source == None or remove_string_source == '':
            remove_string_no_of_selected_photos.config(text = '')
            remove_string_source_label.config(text = 'No Source Selected')
            messagebox.showinfo('No Photos', 'Please Select a Source with a Photo')
            remove_string_window.focus_force()
            remove_string_entry.select_range(0, END)
        
        # if there is a legit source
        elif remove_string_source != None and remove_string_source != '':
            
            # display source folder in text label
            remove_string_source_label.config(text = short_path(remove_string_source))
            
            # build list of photos and sort
            global remove_string_pic_list
            remove_string_pic_list = []
            file_types = ['jpg', 'jpeg', 'png']
            for i in remove_string_files:
                if i.rsplit('.', 1)[1] in file_types:
                    remove_string_pic_list.append(i)
            remove_string_pic_list.sort()
            
            # display number of photos selected
            remove_string_no_of_selected_photos.config(text = f'{len(remove_string_pic_list)} Photos Selected')
            
            # if no actual photos in list
            if len(remove_string_pic_list) == 0:
                remove_string_no_of_selected_photos.config(text = '')
                messagebox.showinfo('No Photos', 'Please Select a Source with a Photo')
            
            # if there are photos in list
            else:
                user_dir = remove_string_source
            remove_string_window.focus_force()
            remove_string_entry.focus()
        
        # if source folder is somehow null
        else:
            remove_string_no_of_selected_photos.config(text = '')
            remove_string_source_label.config(text = 'No Source Selected')
            remove_string_window.focus_force()
            remove_string_entry.select_range(0, END)

    # for keyboard shortcut
    def remove_string_browse_folder_shortcut(event):
        remove_string_browse_folder()
    
    # browse entire folder
    def remove_string_browse_folder():
        global user_dir
        global remove_string_source
        remove_string_source = None
        
        remove_string_source = filedialog.askdirectory(initialdir = user_dir, title = 'Browse Folder')
        
        # if user cancels or somehow selects nothing
        if remove_string_source == None or remove_string_source == '':
            remove_string_no_of_selected_photos.config(text = '')
            remove_string_source_label.config(text = 'No Source Selected')
            messagebox.showinfo('No Photos', 'Please Select a Source with a Photo')
            remove_string_window.focus_force()
            remove_string_entry.select_range(0, END)
        
        # if the user selects a source
        elif remove_string_source != None and remove_string_source != '':
            
            # display source folder in text label
            remove_string_source_label.config(text = short_path(remove_string_source))
            
            # build and sort list of photos
            global remove_string_pic_list
            remove_string_pic_list = []
            remove_string_pic_list = glob(remove_string_source + '/*.jpg')
            remove_string_pic_list.extend(glob(remove_string_source + '/*.jpeg'))
            remove_string_pic_list.extend(glob(remove_string_source + '/*.png'))
            remove_string_pic_list.sort()
            
            # change label for number of photos selected
            remove_string_no_of_selected_photos.config(text = f'{len(remove_string_pic_list)} Photos Selected')
            
            # if there are no photos
            if len(remove_string_pic_list) == 0:
                remove_string_no_of_selected_photos.config(text = '')
                messagebox.showinfo('No Photos', 'Please Select a Source with a Photo')
            
            # if there are photos
            else:
                user_dir = remove_string_source
            remove_string_window.focus_force()
            remove_string_entry.focus()
        
        # if source folder is somehow null
        else:
            remove_string_no_of_selected_photos.config(text = '')
            remove_string_window.focus_force()
            remove_string_entry.select_range(0, END)

    # keyboard shortcut
    def remove_string_shortcut(event):
        remove_string()
    
    # button (or shortcut) activated
    # removes the nth occurrence of a string (from entry) from the beginning or end of photo name
    def remove_string():
        global remove_string_pic_list
        
        # if there are no photos
        if remove_string_pic_list == None or len(remove_string_pic_list) == 0:
            messagebox.showinfo('No Photos', 'Please Select a Source with a Photo')
            remove_string_window.focus_force()
            remove_string_entry.select_range(0, END)
        
        # if nothing in entry box
        elif remove_string_entry.get() == '':
            messagebox.showinfo('No Entry', 'Please enter something to remove')
            remove_string_window.focus_force()
            remove_string_entry.select_range(0, END)
        
        # checks if occurrence # entry is a positive integer
        elif entry_is_pos_int(remove_string_occurrence_entry.get()) == False:
            messagebox.showinfo('Error', 'Please enter a positive integer with no decimals in the "Which Occurrence?" entry box (e.g. "1", "2", etc).')
            remove_string_window.focus_force()
        
        # process to adjust list of photos to fit user settings
        else:
            remove_string_pic_list_adjusted = []
            for i in remove_string_pic_list:
                
                # get filename sans directory
                file_name_with_ext = i.rsplit('/', 1)[1]
                
                # get file name without file extension
                file_name_without_ext = file_name_with_ext.rsplit('.', 1)[0]
                
                # if the number of occurrences of the string to be removed is greater than or equal to the occurrence # to remove, add to adjusted list
                if file_name_without_ext.count(remove_string_entry.get()) >= int(remove_string_occurrence_entry.get()):
                    remove_string_pic_list_adjusted.append(i)
            
            # if adjusted list has no photos
            if len(remove_string_pic_list_adjusted) == 0:
                messagebox.showinfo('Error', f'According to your settings, there are no photos from which to remove the string\n"{remove_string_entry.get()}"')
                remove_string_window.focus_force()
            
            # if adjusted list has photos
            else:
                
                # int n is the occurrence # to remove (which is assured to be int at this point)
                n = int(remove_string_occurrence_entry.get())
                
                # warn user of what will happen
                reply = messagebox.askokcancel('Warning', f'This will remove occurrence #{n} (from the {remove_string_beg_or_end_var.get()} of the filename) of the string\n"{remove_string_entry.get()}"\nfrom the name(s) of {len(remove_string_pic_list_adjusted)} photo(s).')
                
                # if user cancels
                if reply == False:
                    remove_string_window.focus_force()
                    remove_string_entry.select_range(0, END)
                
                # if user proceeds
                else:
                    for i in remove_string_pic_list_adjusted:
                        
                        # split each photo into constituent parts
                        directory_stub = i.rsplit('/', 1)[0]
                        file_name_with_ext = i.split(f'{directory_stub}/', 1)[1]
                        file_name_without_ext = file_name_with_ext.rsplit('.', 1)[0]
                        file_ext = i.rsplit('.', 1)[1]

                        # get string to remove from entry
                        old_string = remove_string_entry.get()

                        # if user wants to remove nth occurrence of old string starting from the beginning of filename
                        if remove_string_beg_or_end_var.get() == 'beginning':
                            
                            # new name part 1 = the first n substrings of filename split by old string n times, joined by old string
                            new_file_name_1 = old_string.join(file_name_without_ext.split(old_string, n)[:n])

                            # new name part 2 = the last substring of filename split by old string n times
                            new_file_name_2 = file_name_without_ext.split(old_string, n)[n]

                        # if user wants to remove nth occurrence of old string starting from the end of filename
                        else:
                            
                            # new name part 1 = the first substring reverse split by old string n times
                            new_file_name_1 = file_name_without_ext.rsplit(old_string, n)[0]

                            # new name part 2 = the second-through-last substrings of filename reverse split by old string n times, joined by old string
                            new_file_name_2 = old_string.join(file_name_without_ext.rsplit(old_string, n)[1:n + 1])
                        
                        # put it together with directory, /, both parts, ., file extension
                        new_name = f'{directory_stub}/{new_file_name_1}{new_file_name_2}.{file_ext}'
                        
                        # make a temporary name
                        temp_name = new_name

                        # start a counter
                        counter = 1

                        # if file already exists
                        while exists(temp_name) == True:

                            # temp name becomes new name without ext + (#) + .file extension
                            temp_name = f'{new_name.rsplit(".", 1)[0]}({counter}).{new_name.rsplit(".", 1)[1]}'

                            # counter goes up by 1
                            counter += 1
                        
                        # once an iteration of the filename does not already exist, assign temp name to new name
                        new_name = temp_name

                        # rename photo with new name
                        rename(i, new_name)
                    
                    # cleanup and reset after process is complete
                    remove_string_pic_list = []
                    remove_string_pic_list_adjusted = []
                    remove_string_no_of_selected_photos.config(text = '')
                    remove_string_source_label.config(text = 'No Source Selected')
                    messagebox.showinfo('Process Complete', 'String has been removed from photo names')
                    remove_string_window.focus_force()
                    remove_string_entry.delete(0, END)
                    remove_string_occurrence_entry.delete(0, END)
                    remove_string_beg.select()
                    remove_string_entry.focus()
    
    # checks if occurrence # is a postive integer
    def entry_is_pos_int(entry):
        try:
            n = int(entry)
            if n > 0:
                return True
            else:
                return False
        except:
            return False

    # tkinter window of 'remove string from photo name' functionality
    remove_string_window = Toplevel(window)
    remove_string_window.geometry('700x250')
    remove_string_window.title('Remove String from Photo Name(s)')

    remove_string_menubar = Menu(remove_string_window)
    remove_string_window.config(menu = remove_string_menubar)
    remove_string_menu = Menu(remove_string_menubar, tearoff = 0)
    remove_string_menu.add_command(label = 'Open File(s)...', command = remove_string_browse_file, accelerator = os_appropriate_command('Cmd-O'))
    remove_string_menu.add_command(label = 'Open Folder...', command = remove_string_browse_folder, accelerator = os_appropriate_command('Cmd-Shift-O'))
    remove_string_menu.add_command(label = 'Remove String from Photo Name(s)', command = remove_string, accelerator = 'Return')
    remove_string_menu.add_command(label = 'Close Remove String Window', command = remove_string_window.destroy, accelerator = os_appropriate_command('Cmd-W'))
    remove_string_menubar.add_cascade(label = 'Remove String', menu = remove_string_menu)
    remove_string_window.bind(os_appropriate_command('<Command-o>'), remove_string_browse_file_shortcut)
    remove_string_window.bind(os_appropriate_command('<Command-Shift-O>'), remove_string_browse_folder_shortcut)
    remove_string_window.bind(os_appropriate_command('<Return>'), remove_string_shortcut)
    remove_string_window.bind(os_appropriate_command('<Command-w>'), close_remove_string_window_shortcut)

    remove_string_browse_label = Label(remove_string_window, text = 'Browse...')
    remove_string_no_of_selected_photos = Label(remove_string_window, text = '')
    remove_string_browse_files_btn = Button(remove_string_window, text = 'Files(s)', command = remove_string_browse_file)
    remove_string_browse_folder_btn = Button(remove_string_window, text = 'Folder', command = remove_string_browse_folder)
    remove_string_source_label = Label(remove_string_window, text = 'No Source Selected', anchor = 'w')
    remove_string_entry_label = Label(remove_string_window, text = 'Enter the exact characters to remove from photo name(s)')
    remove_string_entry = Entry(remove_string_window)
    remove_string_entry.focus()
    remove_string_occurrence_label = Label(remove_string_window, text = 'Which Occurrence?')
    remove_string_occurrence_entry_label_2 = Label(remove_string_window, text = '(enter a positive integer)')
    remove_string_occurrence_entry = Entry(remove_string_window)
    remove_string_occurrence_entry.insert(END, '1')
    remove_string_beg_or_end_label = Label(remove_string_window, text = 'From:')
    remove_string_beg_or_end_var = StringVar(value = 'beginning')
    remove_string_beg = Radiobutton(remove_string_window, text = 'Beginning', variable = remove_string_beg_or_end_var, value = 'beginning')
    remove_string_end = Radiobutton(remove_string_window, text = 'End', variable = remove_string_beg_or_end_var, value = 'end')
    remove_string_button = Button(remove_string_window, text = 'Remove String from Photo Name(s)', default = 'active', command = remove_string)

    remove_string_browse_label.place(x = 30, y = 20)
    remove_string_no_of_selected_photos.place(x = 170, y = 20)
    remove_string_browse_files_btn.place(x = 30, y = 40, width = 70)
    remove_string_browse_folder_btn.place(x = 100, y =40, width = 70)
    remove_string_source_label.place(x = 170, y = 45, width = 530)
    remove_string_entry_label.place(x = 30, y = 70)
    remove_string_entry.place(x = 30, y = 95, width = 230)
    remove_string_occurrence_label.place(x = 30, y = 125)
    remove_string_occurrence_entry.place(x = 160, y = 125, width = 30)
    remove_string_occurrence_entry_label_2.place(x = 190, y = 125)
    remove_string_beg_or_end_label.place(x = 30, y = 155)
    remove_string_beg.place(x = 70, y = 155)
    remove_string_end.place(x = 160, y = 155)
    remove_string_button.place(x = 30, y = 180, width = 230)

    remove_string_window.mainloop()

# for open tutorial shortcut
# calls check_for_tutorial
def tutorial_shortcut(event):
    check_for_tutorial()

# For close tutorial shortcut
# calls tutorial_window.destroy()
def close_tutorial_shortcut(event):
    tutorial_window.destroy()

# activated by Help->Tutorial menu option
# checks to see if tutorial_window already open    
def check_for_tutorial():
    global tutorial_window
    if tutorial_window:
        try:
            tutorial_window.focus_force()
        except:
            tutorial()
    else:
        tutorial()

# called by check_for_tutorial
def tutorial():
    tutorial_dict = {0: ['About the App', 'This app makes it easy to rename individual photos or entire groups of photos. This app will standardize the timestamp format (by extracting metadata) and add the (optional) description of your choice at the end of the filename. Alternatively, you can use only a description.'],
                    1: ['About the App (cont.)', 'Original files may be kept or discarded. If a file with the same name exists, the app will add a number within parentheses at the end of the new file\'s name. This is particularly useful when working with burst shots that have the same timestamp. Other functions include adding or removing arbitrary strings to and from photo filenames.'],
                    2: ['Browse File(s)', f'Click the "File(s)" button ({os_appropriate_command("Cmd-O")}) to select one or more files in a folder for renaming. This app can rename the following file types: jpg, jpeg, png'],
                    3: ['Browse Folder', f'Click the "Folder" button ({os_appropriate_command("Cmd-Shift-O")}) to select all the photos in a folder for renaming. This app can rename the following file types: jpg, jpeg, png'],
                    4: ['Destination Folder', f'Click the "Destination Folder" button ({os_appropriate_command("Cmd-D")}) to find a folder to which renamed photos will be copied. It can be the same folder as the Source Folder.'],
                    5: ['Original File:', 'Select "Discard" if you only want to keep the renamed photo(s). Select "Keep" if you would like to preserve the original photo(s).'],
                    6: ['Rename Photo Using...', 'Select the first option if you would like to rename your photo with the timestamp followed by the (optional) description of your choice. Select the second option if you would like to rename your photo only with the description of your choice. Choosing the latter will disable the options below it.'],
                    7: ['Use Dropdowns To Choose Separators for Exif Timestamp Formatting', 'You can individually choose between several characters to go in between the various parts of the timestamp. Options include a period, hyphen, underscore, space, or nothing at all.'],
                    8: ['If No Exif Timestamp Exists, Rename Photo Using...', 'In case your photo contains no timestamp metadata, this selection will determine what happens. Select the first option to make no changes. Select the second option to preserve the original name followed by the (optional) description of your choice. Select the third option to discard the original name and rename the photo with only the description.'],
                    9: ['Directional Buttons', f'Use these buttons ({os_appropriate_command("Cmd-[")} and {os_appropriate_command("Cmd-]")}) to toggle through the photos in the Source you selected. If you elect to discard the original photo files, they will no longer be available to view after renaming.'],
                    10: ['Enter Photo Description', 'Use the entry field to enter the description of your choice to use in renaming your photos. The app will automatically insert a space between the timestamp and the description. If the field is blank and you elected to use a timestamp, the photo will be renamed with the timestamp only. After every renaming event, the text in the entry field will be deleted.'],
                    11: ['Rename Photo', 'Click the "Rename Photo" button (Return key) to rename the photo. After every photo renaming, the next photo in the Source will display and be ready for renaming.'],
                    12: ['Batch Rename All', f'Click the "Batch Rename All" button ({os_appropriate_command("Cmd-B")}) to rename all the photos in your selection according to the present settings. If you have already renamed any photos and discarded originals, you will be prompted to make a new selection of photos.'],
                    13: ['Add String to Photo Name(s)', f'This functionality is found under the Advanced menu ({os_appropriate_command("Cmd-A")}). Browse for files or folders, enter the exact characters to add to the filename(s), adjust settings, and click the "Add String to Photo Name(s)" button (Return key) to add the string to the names of the relevant photos (at the end, beginning, or after n characters).'],
                    14: ['Remove String from Photo Name(s)', f'This functionality is found under the Advanced menu ({os_appropriate_command("Cmd-R")}). Browse for files or folders, enter the characters to remove from the filename(s), adjust settings, and click the "Remove String from Photo Name(s)" button (Return key) to remove the nth occurrence of the string (from the beginning or end of the filename) from the names of the relevant photos.']
    }
    
    global tutorial_window

    # to ensure buttons activate and deactivate appropriately
    global tutorial_count
    tutorial_count = 0
    min_tutorial_count = 0
    max_tutorial_count = len(tutorial_dict) - 1

    def tutorial_count_down_shortcut(event):
        tutorial_count_down()

    # toggles down through the tutorial titles and descriptions
    def tutorial_count_down():
        global tutorial_count
        
        if tutorial_count == min_tutorial_count:
            pass
        else:
            tutorial_count -= 1
            tutorial_title.config(text = tutorial_dict[tutorial_count][0])
            tutorial_text.config(text = tutorial_dict[tutorial_count][1])
            
            # to make sure previous button disabled on first tutorial entry
            if tutorial_count == min_tutorial_count:
                tutorial_down.config(state = 'disabled')
            
            # to make sure next button active active when not on last tutorial entry
            if tutorial_count <= max_tutorial_count - 1:
                tutorial_up.config(state = 'active', bg = 'white', fg = 'black')

    # for keyboard shortcut
    def tutorial_count_up_shortcutt(event):
        tutorial_count_up()

    # toggles up through the tutorial titles and descriptions
    def tutorial_count_up():
        global tutorial_count
        
        if tutorial_count == max_tutorial_count:
            pass
        else:
            tutorial_count += 1
            tutorial_title.config(text = tutorial_dict[tutorial_count][0])
            tutorial_text.config(text = tutorial_dict[tutorial_count][1])
            
            # to make sure next button disabled on last tutorial entry
            if tutorial_count == max_tutorial_count:
                tutorial_up.config(state = 'disabled')
            
            # to make sure next previous active active when not on first tutorial entry
            if tutorial_count >= min_tutorial_count + 1:
                tutorial_down.config(state = 'active', bg = 'white', fg = 'black')

    # tutorial window
    tutorial_window = Toplevel(window)
    tutorial_window.geometry('300x340')
    tutorial_window.title('Easy Photo Renamer Tutorial')

    # tutorial menu
    tutorial_menubar = Menu(tutorial_window)
    tutorial_window.config(menu = tutorial_menubar)
    tutorial_menu = Menu(tutorial_menubar, tearoff = 0)
    tutorial_menu.add_command(label = 'Next', command = tutorial_count_up, accelerator = os_appropriate_command('Cmd-]'))
    tutorial_menu.add_command(label = 'Previous', command = tutorial_count_down, accelerator = os_appropriate_command('Cmd-['))
    tutorial_menu.add_command(label = 'Close Tutorial', command = tutorial_window.destroy, accelerator = os_appropriate_command('Cmd-W'))
    tutorial_menubar.add_cascade(label = 'Tutorial', menu = tutorial_menu)
    tutorial_window.bind(os_appropriate_command('<Command-]>'), tutorial_count_up_shortcutt)
    tutorial_window.bind(os_appropriate_command('<Command-[>'), tutorial_count_down_shortcut)
    tutorial_window.bind(os_appropriate_command('<Command-w>'), close_tutorial_shortcut)

    # buttons to toggle through tutorial
    tutorial_down = Button(tutorial_window, text = 'Previous', command = tutorial_count_down, state = 'disabled')
    tutorial_up = Button(tutorial_window, text = 'Next', command = tutorial_count_up)

    # tutorial labels
    tutorial_title = Label(tutorial_window, text = tutorial_dict[tutorial_count][0], font = ('SF Pro', 13, 'bold'), wraplength = 250)
    tutorial_text = Label(tutorial_window, text = tutorial_dict[tutorial_count][1], font = ('SF Pro', 13), wraplength = 250)
    
    # closes tutorial window
    tutorial_close_btn = Button(tutorial_window, text = 'Close Tutorial', command = tutorial_window.destroy)

    tutorial_down.place(x = 25, y = 10, anchor = 'nw')
    tutorial_up.place(x = 275, y = 10, anchor = 'ne')

    tutorial_title.place(x = 150, y = 50, anchor = 'n')
    tutorial_text.place(x = 150, y = 120, anchor = 'n')

    tutorial_close_btn.place(x = 150, y = 300, anchor = 'n')

    tutorial_window.mainloop()

# main app window
window = Tk()
window.geometry('1030x500')
window.title(softwareVersion)

# for browse_source and browse_speci_files
global user_dir
user_dir = path.expanduser('~')

# for check_for_tutorial function
global tutorial_window
tutorial_window = None

# for check_for_append_window function
global append_window
append_window = None

# for check_for_remove_string_window function
global remove_string_window
remove_string_window = None

# for copy_pic function
global batch_true
batch_true = False

# for disallowing characters that aren't a good idea to include in filenames
illegal_characters = ('<', '>', ':', '"', '/', '\\', '|', '?', '*')
illegal_characters_warning = 'This app does not allow the use of the following characters in filenames: '
for i in illegal_characters:
    illegal_characters_warning = illegal_characters_warning + i + ' '

# menu
menubar = Menu(window)
window.config(menu = menubar)
file_menu = Menu(menubar, tearoff = 0)
file_menu.add_command(label = 'Browse File(s)...', command = browse_speci_files, accelerator = os_appropriate_command('Cmd-O'))
file_menu.add_command(label = 'Browse Folder...', command = browse_source, accelerator = os_appropriate_command('Cmd-Shift-O'))
file_menu.add_command(label = 'Browse Destination Folder...', command = browse_dest, accelerator = os_appropriate_command('Cmd-D'))
menubar.add_cascade(label = 'File', menu = file_menu)
view_menu = Menu(menubar, tearoff = 0)
view_menu.add_command(label = 'Next Photo', command = count_up, accelerator = os_appropriate_command('Cmd-]'))
view_menu.add_command(label = 'Previous Photo', command = count_down, accelerator = os_appropriate_command('Cmd-['))
menubar.add_cascade(label = 'View', menu = view_menu)
rename_menu = Menu(menubar, tearoff = 0)
rename_menu.add_command(label = 'Rename Photo', command = copy_pic, accelerator = 'Return')
rename_menu.add_command(label = 'Batch Rename Entire Selection', command = batch, accelerator = os_appropriate_command('Cmd-B'))
menubar.add_cascade(label = 'Rename', menu = rename_menu)
advanced_menu = Menu(menubar, tearoff = 0)
advanced_menu.add_command(label = 'Add String to Photo Name(s)...', command = check_for_append_window, accelerator = os_appropriate_command('Cmd-A'))
advanced_menu.add_command(label = 'Remove String from Photo Names(s)...', command = check_for_remove_string_window, accelerator = os_appropriate_command('Cmd-R'))
menubar.add_cascade(label = 'Advanced', menu = advanced_menu)
help_menu = Menu(menubar, tearoff = 0)
help_menu.add_command(label = 'Tutorial', command = check_for_tutorial, accelerator = os_appropriate_command('Cmd-T'))
menubar.add_cascade(label = 'Help', menu = help_menu)
window.bind(os_appropriate_command('<Command-o>'), browse_speci_files_shortcut)
window.bind(os_appropriate_command('<Command-Shift-O>'), browse_source_shortcut)
window.bind(os_appropriate_command('<Command-d>'), browse_dest_shortcut)
window.bind(os_appropriate_command('<Command-b>'), batch_shortcut)
window.bind(os_appropriate_command('<Command-t>'), tutorial_shortcut)
window.bind(os_appropriate_command('<Command-]>'), count_up_shortcut)
window.bind(os_appropriate_command('<Command-[>'), count_down_shortcut)
window.bind('<Return>', copy_pic_shortcut)
window.bind(os_appropriate_command('<Command-b>'), batch_shortcut)
window.bind(os_appropriate_command('<Command-a>'), append_window_shortcut)
window.bind(os_appropriate_command('<Command-r>'), remove_string_window_shortcut)

# photos will not display larger than this
max_size = (300, 300)

browse_lbl = Label(window, text = 'Browse...')

# label to display number of photos selected
number_of_pics = Label(window, text = '')

browse_speci_files_btn = Button(text = 'File(s)', command = browse_speci_files)

# chooses source folder
browse_source_btn = Button(text = 'Folder', command = browse_source)

# displays source folder
source_lbl = Label(window, text = 'No Source Selected', anchor = 'w')

# chooses destination folder
browse_dest_btn = Button(text = 'Destination Folder', command = browse_dest)

# displays destination folder
dest_lbl = Label(window, text = 'No Destination Folder Selected', anchor = 'w')

# label and radiobutton options for either keeping or discarding original file
keep_or_no_lbl = Label(window, text = 'Original File:')
keep_var = StringVar(value = 'Discard')
discard_original = Radiobutton(window, text = 'Discard', variable = keep_var, value = 'Discard')
keep_original = Radiobutton(window, text = 'Keep', variable = keep_var, value = 'Keep')

# label and radiobutton options for either renaming with timestamp & description or description only
date_or_no_lbl = Label(window, text = 'Rename Photo Using...')
time_stamp_var = StringVar(value = 'Timestamp & Description')
dateAndDescription = Radiobutton(window, text = 'Timestamp & Description', variable = time_stamp_var, value = 'Timestamp & Description', command = timestamp_or_no)
description_only = Radiobutton(window, text = 'Description Only', variable = time_stamp_var, value = 'Description Only', command = timestamp_or_no)

date_format_lbl = Label(window, text = 'Use Dropdowns To Choose Separators for Exif Timestamp Formatting')

# all options for date formatting separators
options_dict = {
    '.': '.',
    '-': '-',
    '_': '_',
    '[ ]': ' ',
    'NULL': ''
}

# labels and dropdowns for seleting timestamp separators
year_lbl = Label(window, text = 'YYYY')
ym = StringVar()
ym.set('[ ]')
year_month_dropdown = OptionMenu(window, ym, *options_dict)
year_month_dropdown.config(width = 2)
month_lbl = Label(window, text = 'MM')
md = StringVar()
md.set('-')
month_day_dropdown = OptionMenu(window, md, *options_dict)
month_day_dropdown.config(width = 2)
day_lbl = Label(window, text = 'DD')
dh = StringVar()
dh.set('[ ]')
day_hour_dropdown = OptionMenu(window, dh, *options_dict)
day_hour_dropdown.config(width = 2)
hour_lbl = Label(window, text = 'HH')
hm = StringVar()
hm.set('.')
hour_min_dropdown = OptionMenu(window, hm, *options_dict)
hour_min_dropdown.config(width = 2)
min_lbl = Label(window, text = 'MM')
ms = StringVar()
ms.set('.')
min_sec_dropdown = OptionMenu(window, ms, *options_dict)
min_sec_dropdown.config(width = 2)
sec_lbl = Label(window, text = 'SS')

# label and radiobutton options for selecting either original name & description or description only in case of no timestamp metadata
if_no_exif_lbl = Label(window, text = 'If No Exif Timestamp Exists, Rename Photo Using...')
if_no_exif_var = StringVar(value = 'Original Name Only')
original_only = Radiobutton(window, text = 'Original Name Only (Change Nothing)', variable = if_no_exif_var, value = 'Original Name Only')
original_and_description = Radiobutton(window, text = 'Original Name & Description', variable = if_no_exif_var, value = 'Original Name & Description')
no_original_description_only = Radiobutton(window, text = 'Description Only', variable = if_no_exif_var, value = 'Description Only')

# go through main_pic_list either ascending or descending
count_down_btn = Button(window, text = '←', state = 'disabled', command = count_down)
count_up_btn = Button(window, text = '→', state = 'disabled', command = count_up)

# contains image and image title
pic_frame = Frame(window, height = 500, width = 300)

# open default pic and display in window
img = ImageOps.exif_transpose(Image.open('PicRenamerDefaultPic.png'))
img.thumbnail(max_size)
img = ImageTk.PhotoImage(img)
pic_lbl = Label(pic_frame, image = img)

# for displaying name of the photo
pic_name_lbl = Label(pic_frame, text = '')

# where user inputs photo description
fieldLbl = Label(pic_frame, text = 'Enter Photo Description')
enter_new_name = Entry(pic_frame)
enter_new_name.select_range(0, END)

# buttons to do the thing
copy_pic_btn = Button(pic_frame, text = 'Rename Photo', default = 'active', command = copy_pic)
batch_rename_btn = Button(pic_frame, text = 'Batch Rename All', command = batch)

browse_lbl.place(x = 30, y = 20)
number_of_pics.place(x = 170, y = 20)
browse_speci_files_btn.place(x = 30, y = 40, width = 70)
browse_source_btn.place(x = 100, y = 40, width = 70)
source_lbl.place(x = 170, y = 45, width = 530)
browse_dest_btn.place(x = 30, y = 70, width = 140)
dest_lbl.place(x = 170, y = 75, width = 530)

keep_or_no_lbl.place(x = 30, y = 129)
discard_original.place(x = 30, y = 149)
keep_original.place(x = 30, y = 169)

date_or_no_lbl.place(x = 30, y = 223)
dateAndDescription.place(x = 30, y = 243)
description_only.place(x = 30, y = 263)

date_format_lbl.place(x = 30, y = 317)
year_lbl.place(x = 30, y = 342)
year_month_dropdown.place(x = 70, y = 342)
month_lbl.place(x = 132, y = 342)
month_day_dropdown.place(x = 162, y = 342)
day_lbl.place(x = 224, y = 342)
day_hour_dropdown.place(x = 249, y = 342)
hour_lbl.place(x = 311, y = 342)
hour_min_dropdown.place(x = 336, y = 342)
min_lbl.place(x = 398, y = 342)
min_sec_dropdown.place(x = 428, y = 342)
sec_lbl.place(x = 490, y = 342)

if_no_exif_lbl.place(x = 30, y = 395)
original_only.place(x = 30, y = 415)
original_and_description.place(x = 30, y = 435)
no_original_description_only.place(x = 30, y = 455)

count_down_btn.place(x = 735, y = 20, width = 50)
count_up_btn.place(x = 965, y = 20, width = 50, anchor = 'ne')

pic_frame.place(x = 700, y = 50)
pic_lbl.place(x = 150, y = 150, anchor = 'center')
pic_name_lbl.place(x = 150, y = 320, anchor = 'center')

fieldLbl.place(x = 150, y = 360, anchor = 'center')
enter_new_name.place(x = 150, y = 385, anchor = 'center')
copy_pic_btn.place(x = 15, y = 412, width = 134, anchor = 'w')
batch_rename_btn.place(x = 285, y = 412, width = 134, anchor = 'e')

window.mainloop()
