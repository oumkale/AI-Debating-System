#!/usr/bin/env python
# coding: utf-8

# In[27]:


import speech_recognition as sr
from gtts import gTTS 
import os


# In[28]:


r = sr.Recognizer()

    #recognize_bing()
    #recognize_google()
    #recognize_google_cloud()
    #recognize_ibm()
    #recognize_sphinx()


# In[ ]:


filename ="16-122828-0002.wav"


# In[3]:


# import os
# from pocketsphinx import LiveSpeech, get_model_path


# In[4]:


# from pocketsphinx import LiveSpeech
# for phrase in LiveSpeech(): print(phrase)


# In[29]:


with sr.Microphone() as source:
    audio_data = r.record(source, duration=5)
    print("Recognizing...")
    
    r.adjust_for_ambient_noise(source)
    text = r.recognize_google(audio_data)
    print(text)


# In[30]:


with sr.AudioFile(filename) as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data)
    print(text)


# In[31]:


with sr.Microphone() as source:
    print("Say something!")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)


# In[33]:


get_ipython().run_cell_magic('time', '', 'try:\n    #r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`\n    print("You said: " + r.recognize_google(audio))\nexcept sr.UnknownValueError:\n    print("Google Speech Recognition could not understand audio")\nexcept sr.RequestError as e:\n    print("Could not request results from Google Speech Recognition service; {0}".format(e))')


# In[1]:


from gtts import gTTS 
import os


# In[25]:


get_ipython().run_cell_magic('time', '', 'intro = \'Welcome! so tell me, what would we be debating on today?\'\nspeech = gTTS(text = intro, lang = \'en-in\', slow = False)\nspeech.save("Intro.mp3")')


# In[ ]:





# In[ ]:


os.system("mpg321 text.mp3")


# In[ ]:





# In[ ]:




