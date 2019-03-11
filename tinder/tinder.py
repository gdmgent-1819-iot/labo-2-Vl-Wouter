import requests, json
from sense_hat import SenseHat
import time
import sys

sense = SenseHat()

# Function to load saved data in json file
def loadData():
  with open('data.json') as json_data:
    data = json.load(json_data)
    return data

# Function to get and display a user from the API
def getUser():
  request = requests.get('https://randomuser.me/api').json()
  data = request['results'][0]
  nameData = data['name']
  name = nameData['first'] + " " + nameData['last']
  sense.show_message(name)
  return name

# Function to save data back to json file
def saveData(user, choice, dataset):
  data = dataset
  if(choice == 'liked'):
    data['liked'].append(user)
  else:
    data['disliked'].append(user)
  with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
  
# Main application function
def main():
  try:
    data = loadData()
    user = getUser()
    events = sense.stick.get_events()
    if(len(events) != 0):
      choiceEvent = events[0]
    else:
      choiceEvent = sense.stick.wait_for_event()
    if(choiceEvent.direction == 'right'):
      choice = 'disliked'
    else:
      choice = 'liked'
    saveData(user, choice, data)
    time.sleep(1)
    main()
  except KeyboardInterrupt:
    print('Interrupting process')
    sense.clear()
    sys.exit(0)
    
  
main()