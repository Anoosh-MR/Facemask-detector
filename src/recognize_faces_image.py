# USAGE
# python recognize_faces_image.py --encodings encodings.pickle --image examples/example_01.png 

# import the necessary packages
import face_recognition
import argparse
import pymysql
import pickle
import cv2
passwd='123456789'
con=pymysql.connect(host="localhost",user="root",password=passwd,port=3308,db="mask_violation")
cmd=con.cursor()
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-e", "--encodings", required=True,
# 	help="path to serialized db of facial encodings")
# ap.add_argument("-i", "--image", required=True,
# 	help="path to input image")
# ap.add_argument("-d", "--detection-method", type=str, default="cnn",
# 	help="face  detection model to use: either `hog` or `cnn`")
# arg s = vars(ap.parse_args())

# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open('abc.pickle', "rb").read())

class facerec():
	def facerecg(self,img):
		# load the input image and convert it from BGR to RGB
		image = cv2.imread(img)
		h, w, ch = image.shape
		print(ch)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# detect the (x, y)-coordinates of the bounding boxes corresponding
		# to each face in the input image, then compute the facial embeddings
		# for each face
		print("[INFO] recognizing faces...")
		boxes = face_recognition.face_locations(rgb,model='hog')
		encodings = face_recognition.face_encodings(rgb, boxes)

		# initialize the list of names for each face detected
		names = []

		# loop over the facial embeddings
		for encoding in encodings:
			# attempt to match each face in the input image to our known
			# encodings
			matches = face_recognition.compare_faces(data["encodings"],
													 encoding,tolerance=.4)
			name = "Unknown"

			# check to see if we have found a match
			if True in matches:
				# find the indexes of all matched faces then initialize a
				# dictionary to count the total number of times each face
				# was matched
				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}

				# loop over the matched indexes and maintain a count for
				# each recognized face face
				for i in matchedIdxs:
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1






				# determine the recognized face with the largest number of
				# votes (note: in the event of an unlikely tie Python will
				# select first entry in the dictionary)

				uid = name;
				# cmd.execute("select * from attendance where uid==name")
				qry="select * from attendance where sid='"+ uid+"' and date=curdate()"
				cmd.execute(qry)
				s=cmd.fetchone()
				if (s is not  None):
					cmd.execute("update attendance set logouttime=curtime() where id='"+str(s[0])+"'")
					con.commit()

				else:
					cmd.execute("insert into attendance values(null,'" + uid + "',curdate(),'1',curtime(),NULL)")
					con.commit()

				name = max(counts, key=counts.get)
				print(name, "names")

			# update the list of names
			# if name not in names:
			names.append(name)

			print(names, "names are")
		# loop over the recognized faces
		for ((top, right, bottom, left), name) in zip(boxes, names):
			# draw the predicted face name on the image
			cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
						0.75, (0, 255, 0), 2)

		# show the output image
		cv2.imshow("Image", image)
		cv2.waitKey(0)
