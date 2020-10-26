'''
# Here are all the installs and imports you will need for your word cloud script and uploader widget
!pip install wordcloud
!pip install fileupload
!pip install ipywidgets
!jupyter nbextension install --py --user fileupload
!jupyter nbextension enable --py fileupload
'''
import wordcloud
import numpy as np
from matplotlib import pyplot as plt
from IPython.display import display
import fileupload
import io
import sys



# This is the uploader widget

def _upload():

    _upload_widget = fileupload.FileUploadWidget()

    def _cb(change):
        global file_contents
        decoded = io.StringIO(change['owner'].data.decode('utf-8'))
        filename = change['owner'].filename
        print('Uploaded `{}` ({:.2f} kB)'.format(
            filename, len(decoded.read()) / 2 **10))
        file_contents = decoded.getvalue()

    _upload_widget.observe(_cb, names='data')
    display(_upload_widget)

_upload()

def calculate_frequencies(file_contents):
    # Here is a list of punctuations and uninteresting words we will use to process the text
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    uninteresting_words = ["the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my", \
    "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its", "they", "them", \
    "their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be", "been", "being", \
    "have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when", "where", "how", \
    "all", "any", "both", "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just"]
    
    new_text = ""
    for char in file_contents:
        if char not in punctuations:
            new_text = new_text + char
    words = new_text.split()
    clean_words = []
    d = {}
    for word in words:
        if word.isalpha():
            if word not in uninteresting_words:
                clean_words.append(word)
    for alpha_word in clean_words:
        if alpha_word not in d:
            d[alpha_word] = 1
        else:
            d[alpha_word] += 1
    print(d)
    
    cloud = wordcloud.WordCloud()
    cloud.generate_from_frequencies(d)
    return cloud.to_array()
#This is the string you have to provide to generate the word cloud.
file_contents = "On my pillow Can't get me tired Sharing my fragile truth That I still hope the door is open 'Cause the window Opened one time with you and me \
                 Now my forever's falling down Wondering if you'd want me now How could I know One day I'd wake up feeling more But I had already reached the shore \
                 Guess we were ships in the night Night, night We were ships in the night, night, night I'm wondering Are you my best friend  \
                 Feel's like a river's rushing through my mind I wanna ask you If this is all just in my head My heart is pounding tonight I wonder If you \
                 Are too good to be true And would it be alright if I Pulled you closer How could I know One day I'd wake up feeling more \
                 But I had already reached the shore Guess we were ships in the night Night, night We were ships in the night Night, night" 
 
myimage = calculate_frequencies(file_contents)
plt.imshow(myimage, interpolation = 'nearest')
plt.axis('off')
plt.show()
