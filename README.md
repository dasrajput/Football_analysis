### Development Manual for Football Analysis Project

---

## **Important: Please Read Carefully**
This manual contains instructions to help you set up and run the project efficiently. Note that it takes approximately **6-7 minutes** to generate the output video for the first time due to model processing and stub generation. Ensure that you follow each step accurately to avoid any issues during development.

---

### 1. **Project Overview**
   This project uses machine learning models to analyze football match data. We employ object detection, tracking, camera movement estimation, and other analytical methods to produce insightful outputs such as player speeds, distances covered, and team assignments.

### 2. **Project Structure**
   The project is organized into the following key directories:
   - `Input_Videos/`: Contains the raw football videos for analysis.
   - `Output_Videos/`: Stores the output videos with annotations and insights.
   - `models/`: Contains the trained model weights (e.g., `best.pt` for YOLO object detection).
   - `stubs/`: Stores precomputed results (e.g., object tracks, camera movement) for faster processing of previously analyzed videos.

### 3. **Setting Up the Environment**

#### **Prerequisites**
   1. **Python**: Ensure Python 3.x is installed on your system.
   2. **Git**: Make sure Git is installed to clone and manage repositories.

#### **Installation Steps**
1. **Fork the Repository**:
   - Go to the GitHub repository and click the "Fork" button to create a copy of the repository in your GitHub account.
   - Here’s a [YouTube tutorial](https://www.youtube.com/watch?v=f5grYMXbAV0) on how to fork a repository.

2. **Clone Your Fork**:
   - Clone your forked repository using Git:  
     ```bash
     git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
     cd REPO_NAME
     ```
   - Replace `YOUR_USERNAME` and `REPO_NAME` with your GitHub username and repository name.

3. **Install Dependencies**:
   Run the following commands to install the required Python libraries:
   ```bash
   pip install ultralytics supervision opencv-python-headless numpy matplotlib pandas
   ```

4. **Set Up VS Code**:
   - Open the project in VS Code:  
     ```bash
     code .
     ```
   - Follow this [YouTube guide](https://www.youtube.com/watch?v=iv8rSLsi1xo) to learn how to connect VS Code with GitHub for better version control.

### 4. **Workflow and Best Practices**

#### **Branching Strategy**:
   - **Main Branch**: The main branch is stable and shouldn't be changed directly. **Do not push directly to the main branch**.
   - **Default Branch**: Work on the latest branch (default branch). Fork the repository and make your changes here.
   - **Push/Pull Requests**: After making changes, push them to your forked repository and create a pull request back to the main repository. Here's a [tutorial on pull requests](https://www.youtube.com/watch?v=rgbCcBNZcdQ).

#### **Commit Guidelines**:
   - Keep commit messages clear and concise.
   - Use messages like: `Added camera movement estimation logic` or `Fixed bug in speed calculation`.

#### **Collaboration Tips**:
   - Always **pull the latest changes** before starting any work to avoid conflicts:  
     ```bash
     git pull origin branch_name
     ```
   - **Merge conflicts** are common in collaborative projects. Learn how to resolve them [here](https://www.youtube.com/watch?v=JtIX3HJKwfo).

### 5. **Running the Project**

#### **Step-by-Step Instructions**:
1. **Video Input**:
   - Place your football match video in the `Input_Videos/` folder.
   - Update the input video path in `main.py`:
     ```python
     video_frames = read_video('Input_Videos/YOUR_VIDEO.mp4')
     ```

2. **Stub Handling**:
   - When processing a new video, generate new stub files by renaming them appropriately, such as:
     ```python
     stub_path = 'stubs/track_stubs_YOUR_VIDEO.pkl'
     ```

3. **Run the Project**:
   - To process the video and generate outputs, run:
     ```bash
     python main.py
     ```

4. **Output Video**:
   - After processing, the output video will be saved in `Output_Videos/` as `YOUR_VIDEO_out.avi`.

#### **Stub Optimization**:
   - **Stubs** store precomputed detection results for faster processing. When analyzing the same video again, the project will use the stored stubs, significantly reducing the processing time.
   - Ensure that you correctly name your stubs as described earlier to prevent overwriting or errors.

### 6. **Module Descriptions**

#### **Key Modules Used**:
- **YOLO**: AI object detection model for tracking players and the ball.
- **Kmeans**: Used for segmenting and clustering pixels to detect player t-shirt colors.
- **Optical Flow**: Measures the movement of the camera during the match.
- **Perspective Transformation**: Handles depth and perspective to produce a realistic view.
- **Speed and Distance Calculation**: Provides estimates of player speed and distance covered during the match.

---

### 7. **Useful Resources**
- **YOLO Tutorial**: [YOLO Documentation](https://docs.ultralytics.com/)
- **Git and GitHub for Beginners**: [GitHub Learning Lab](https://lab.github.com/)
- **Object Detection with OpenCV**: [OpenCV Documentation](https://docs.opencv.org/)

---

By following this manual, you'll be able to get started quickly and work collaboratively on the Football Analysis Project. Take your time, and if you have questions, don't hesitate to ask the team for help.
