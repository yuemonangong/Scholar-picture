In Crawler directory:
	Codes in crawler-final-version directory are the final version scholar pictures crawler we use. Run execute.py to get the scholar pictures from websites.
	Codes in temp directory are all the temporary codes.

In Recognition dictionary£º
	dlib folder contains the realization of the dlib methods.
	facenet folder contains the realization of the facenet methods.
	Haar-LBP folder contains the realization of the Haar detection and the LBP descriptor extraction.
	Because the dataset is too large, we cannot upload to github. Hence if wanna to run the code you should rewrite the file part.
	In dlib and Haar-LBP, you should run face-filt code first and then run face-cluster code. You should decompression the dlib model from the dlibmodel.rar.
	In facenet, you just need to run face_all_facenet code. This part extracts the key codes from facenet and packages them for use, so the model provided by facenect needs to be submitted for download. Now the model is saved in baidu network disk: https://pan.baidu.com/s/1i4YhAdB?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0&traceid=#list/path=%2F
and the password is avbl, store it in the directory structure of models\facenet\20170512-110547.