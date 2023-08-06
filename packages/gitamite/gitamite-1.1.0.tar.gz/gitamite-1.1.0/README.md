# gitamite-library
This library can fetch data from Moodle and Glearn. Timetable, Upcoming activites, Homepage for now. Will be adding more. 
 
 # Installation
 ```
pip install gitamite
```
# Usage
### Moodle
 ```
from gitamite import Moodle

m = Moodle()

m.username = 'your_username'
m.password = 'your_password'

m.loginMoodle()
homepage = m.getMoodleHomepage()
upcomingActivities = m.getUpcomingActivities()
isLoggedIn = m.isMoodleLoggedIn()
m.logoutMoodle()
```
### GLearn
```
from gitamite import Glearn

g = Glearn()

g.username = 'your_username'
g.password = 'your_password'

g.loginGlearn()
timetable = g.getTimetable()
timetableToday = g.getTimetableToday()
isLoggedIn = g.isGlearnLoggedIn()
```
