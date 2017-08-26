import glob
import os
import sys
import argparse
import piexif

################################################################################
# Pseudocode
################################################################################
# X Check if directory argument has been passed
# X If no directory argument has been passed get the working directory
# X Look for .jpg and .jpeg files in the directory & load file names
# X Iterate over image names and remove exif data
# Check exif data has been removed for each file
################################################################################
# Main Function
def main():
	# Check if the script is running as standalone
	if __name__ == "__main__":
		# Check if no arguments are passed
		if len(sys.argv) == 1:
			# Set source directory to the current working directory
			source_dir = str(os.getcwd())
			print("[+] No working directory passed. Setting source directory to current working directory")
	
		# Check if arguments were passed
		else:
			# Set the source directory to the provided value
			source_dir = str(sys.argv[1])

			# Check if passed argument is a valid diectory
			if not os.path.isdir(source_dir):
				print("[-] ERROR: Argument is not a valid directory : " + source_dir)
				sys.exit()
			else:		
				print("[+] Setting source directory to: " + source_dir)

		# Search for .jpg and .jpeg files in source directory
		print("[+] Searching for images files in " + source_dir)
		found_images = search_image_files(source_dir)

		# Check if returned list is empty
		if not found_images:
			print("[-] ERROR: No image files found! Exiting")
			sys.exit()

		# Strip exif data from found images
		print("[+] Stripping EXIF data from image files")
		strip_exif(found_images, source_dir)

		# Verify that EXIF data has been stripped
		print("[+] Verifying EXIF data has been removed")
		check_exif(found_images, source_dir)

# Function to search for image files
def search_image_files(directory):
	# List of jpeg file extentions to search for
	extentions = ['.jpg', '.JPG', '.jpeg', '.JPEG']

	# Create variable for image file names
	image_files = []

	# Iterate over extensions and search for files in the directory with a matching extension
	for extention in extentions:
		# Change to source directory
		os.chdir(directory)

		# Temporary variable to store found file names
		file_names = glob.glob('**/*' + extention, recursive=True)

		# Check if files were found, and if so add the found files to the image file list
		if file_names:
			for file in file_names:
				image_files.append(file)

	return(image_files)

# Function to strip EXIF data
def strip_exif(file_list, directory):
	# Iterate over files names in list
	for index in range(len(file_list)):
		full_file_path = directory + "/" + str(file_list[index])
		
		# Strip EXIF data from file
		piexif.remove(full_file_path)

# Function to check if EXIF data has been removed
def check_exif(file_list, directory):
	# Iterate over files names in list
	for index in range(len(file_list)):
		full_file_path = directory + "/" + str(file_list[index])

		print("\tEXIF data for " + full_file_path)
		print("\t\t" + str(piexif.load(full_file_path)))

# Run the main function
main()