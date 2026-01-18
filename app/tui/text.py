from rich.markdown import Markdown
from rich.panel import Panel

welcome = Panel(Markdown('''
# 🚀 WELCOME TO CLUBHUB!!!! 🚀

## 🏫 Campus-Focused Club Management
**ClubHub** is the unified platform for **IIIT Sri City**, designed to replace scattered communication with structured, institute-focused collaboration.

## 👥 Team & Tech
- **Developed By**: Epoch Innovators (Aarush & Tanay)

## ⭐ Key Features
- **💬 Institute-Only Chat**: Verified, distraction-free communication spaces.
- **📅 Event Management**: Centralized RSVPs, scheduling, and attendance tracking.
- **🏆 Gamified Engagement**:
  - **Daily Questions**: Earn **+1 point** per answer.
  - **Volunteering**: High-value contributions earn **+10 to +20 points**.
  - **Leaderboards**: Monthly resets to keep competition fair and active.
- **📊 Analytics**: Track your participation and club growth over time.

> "A platform designed for clubs, not a generic chat server."
'''))


login = Panel(Markdown('''
# 🔐 CLUBHUB AUTHENTICATION PORTAL

##  User Login/Sign Up
### (1) **🆕 Create a New Account**
### (2) **👤 Login with an Existing Account**
### (3) **👋 Go back to Welcome Page**

---
*Select an option (1-3) to proceed*
'''))

homepage = Panel(Markdown('''
# 🏠 CLUBHUB DASHBOARD

### 1️⃣ Create New Club
Start a new community at **IIIT Sri City**.
- **🔒 Restriction:** Requires an **Admin Secret Key**.
- **👑 Outcome:** You will be automatically assigned as the **Club Lead**.

### 2️⃣ Your Active Clubs
Access the clubs you are currently a member of.
- View **Private Chats** & **Announcements**
- Check your **Points** & **Leaderboard Rank**

### 3️⃣ Browse Campus
Explore other clubs and see what's happening.
- View **Public Announcements**
- Request to join new communities
- See upcoming campus-wide events

---
*Select an option (1-3) to proceed*
'''))


clubpage = Panel(Markdown("""
# 🛡️ CLUBPAGE

### Select an option:

**[1] All Channels 📺**  
Browse and access available club channels.

**[2] Leaderboard 🏆**  
Rankings based on participation and contributions.

**[3] Attendance Records 📋**  
Attendance and participation history.

**[4] View Users 👤** 
Create a new discussion or project channel.

**[5] Go back to Club Page 👋**
"""))