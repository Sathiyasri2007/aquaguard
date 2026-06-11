# 📱 Dashboard User Guide

## Welcome to Smart Community Health Monitoring System

This guide will help you navigate and use the dashboard effectively.

## 🎯 Dashboard Overview

The system has 4 main tabs:
1. **Water Analysis** - Upload and analyze water samples
2. **Risk Map** - View geographic risk distribution
3. **Alert Dashboard** - Monitor alerts and responses
4. **NGO Management** - Manage NGO contacts and responses

---

## Tab 1: Water Analysis 🔬

### Purpose
Analyze water sample images to detect contamination and predict diseases.

### How to Use

#### Step 1: Upload Image
1. Click on the upload area (dashed border)
2. Select a water sample image (JPG or PNG)
3. Preview will appear below

#### Step 2: Enter Location Details
1. **Location**: Type the location name
   - Example: "Guwahati Village Well"
   - Example: "Dibrugarh River Point"

2. **Latitude**: Enter latitude coordinate
   - Example: 26.2006
   - Use GPS or Google Maps to find coordinates

3. **Longitude**: Enter longitude coordinate
   - Example: 92.9376

#### Step 3: Analyze
1. Click "Analyze Water Sample" button
2. Wait 2-3 seconds for processing
3. Results will appear in two sections:

### Understanding Results

#### Analysis Results Box
- **Classification**: Safe / Possibly Contaminated / Contaminated
- **Confidence**: Percentage (higher = more certain)
- **Water Quality**: Pure / Moderately Unsafe / Highly Contaminated
- **Risk Level**: 🔴 High / 🟡 Medium / 🟢 Low

#### Visual Indicators
- **Turbidity**: Low (clear) / High (cloudy)
- **Color**: Normal (blue) / Abnormal (brown/green)
- **Floating Waste**: None / Detected
- **Oil Layer**: None / Detected
- **Algae**: None / Detected

#### Disease Predictions
For each disease, you'll see:
- **Disease Name**: e.g., Cholera, Typhoid
- **Risk Score**: Percentage likelihood
- **Severity**: Critical / High / Medium
- **Symptoms**: List of symptoms to watch for
- **Prevention**: Steps to prevent infection

### What Happens Next?
- If contamination is detected, an alert is automatically created
- NGOs are notified via email and SMS
- Location is added to the risk map
- Data is stored for pattern analysis

---

## Tab 2: Risk Map 🗺️

### Purpose
Visualize geographic distribution of water contamination risk across regions.

### How to Use

#### View the Map
1. Click "Risk Map" tab
2. Map loads automatically
3. Click "Refresh Map" to update with latest data

#### Understanding the Map

##### Markers
- 🔴 **Red Circle**: High Risk location
  - Highly contaminated water
  - Multiple disease risks
  - Immediate action needed

- 🟡 **Orange Circle**: Medium Risk location
  - Moderately unsafe water
  - Some disease risks
  - Monitoring required

- 🟢 **Green Circle**: Low Risk location
  - Safe water quality
  - No immediate concerns
  - Continue monitoring

##### Marker Information
Click any marker to see:
- Location name
- Risk level
- Water quality status
- Number of diseases detected
- Last update time

#### Risk Patterns Section
Below the map, you'll see:
- **High Risk Locations**: Top 5 risky areas
- **Risk Score**: Numerical risk assessment
- **Contamination Incidents**: Number of contamination events
- **Average Diseases**: Average diseases per incident

### Using the Information
- Identify areas needing immediate attention
- Plan resource allocation
- Track contamination trends
- Monitor intervention effectiveness

---

## Tab 3: Alert Dashboard 🚨

### Purpose
Monitor alerts, track responses, and view system performance.

### Dashboard Statistics (Top Cards)

#### Total Alerts
- Number of alerts generated
- Includes all statuses

#### Responded
- Alerts with NGO responses
- Shows system effectiveness

#### Pending
- Alerts awaiting response
- Requires attention

#### Avg Response
- Average response time in hours
- Lower is better

### Alert History

#### Alert Status Colors
- **Yellow Background**: Pending (awaiting response)
- **Green Background**: Responded (action taken)
- **Red Background**: Escalated (overdue, no response)

#### Alert Information
Each alert shows:
- **Alert ID**: Unique identifier (e.g., ALT20240115123045)
- **Location**: Where contamination was detected
- **Time**: When alert was created
- **Status**: Pending / Responded / Escalated
- **Risk Level**: High / Medium / Low
- **Diseases**: List of potential diseases

### Monitoring Tips
- Check pending alerts daily
- Follow up on escalated alerts immediately
- Review response times weekly
- Identify patterns in alert locations

---

## Tab 4: NGO Management 👥

### Purpose
Register NGOs and record their responses to alerts.

### Section 1: Register NGO

#### How to Register
1. **NGO Name**: Enter organization name
   - Example: "Health First NGO"

2. **Email**: Enter contact email
   - Example: "contact@healthngo.org"
   - Used for alert notifications

3. **Phone Number**: Enter phone with country code
   - Example: "+91-9876543210"
   - Used for SMS alerts

4. **Region**: Enter coverage area
   - Example: "Guwahati District"

5. Click "Register NGO"
6. Note the NGO ID returned (needed for responses)

### Section 2: Record Response

#### When to Use
- NGO has taken action on an alert
- Need to document response time
- Track intervention effectiveness

#### How to Record
1. **Alert ID**: Enter the alert ID
   - Found in Alert Dashboard
   - Format: ALT20240115123045

2. **NGO ID**: Enter the NGO's ID
   - Received during registration
   - Example: 1, 2, 3, etc.

3. **Action Taken**: Describe the response
   - Example: "Distributed water purification tablets"
   - Example: "Sent medical team, warned community"
   - Example: "Arranged alternative water source"

4. Click "Submit Response"

#### What Happens
- Response time is calculated
- Alert status changes to "Responded"
- Statistics are updated
- Response is logged for analysis

---

## 💡 Best Practices

### For Water Analysis
1. **Image Quality**
   - Use clear, well-lit photos
   - Capture water surface clearly
   - Avoid shadows and reflections
   - Take photos in daylight

2. **Location Accuracy**
   - Use GPS for precise coordinates
   - Include landmark in location name
   - Be consistent with naming

3. **Regular Monitoring**
   - Test same locations weekly
   - Track changes over time
   - Document seasonal variations

### For Alert Management
1. **Response Time**
   - Aim for < 24 hours
   - Prioritize high-risk alerts
   - Escalate if no response

2. **Documentation**
   - Record all actions taken
   - Include details in responses
   - Track outcomes

3. **Follow-up**
   - Re-test water after intervention
   - Monitor disease reports
   - Update community

### For NGO Coordination
1. **Registration**
   - Register all partner NGOs
   - Keep contact info updated
   - Define coverage areas clearly

2. **Communication**
   - Check emails regularly
   - Respond to alerts promptly
   - Report back on actions

3. **Collaboration**
   - Share resources
   - Coordinate responses
   - Learn from each case

---

## 🔔 Alert Notifications

### Email Alerts
NGOs receive emails with:
- Alert ID and timestamp
- Location and coordinates
- Risk level and water quality
- List of potential diseases
- Severity level
- Response deadline

### SMS Alerts
Short message with:
- Location
- Risk level
- Top diseases
- Alert ID

### Response Required
- Acknowledge receipt
- Take appropriate action
- Record response in system
- Report outcomes

---

## 📊 Understanding Risk Scores

### Risk Score Calculation
```
Risk Score = (Contamination Events × 0.4) +
             (Average Diseases × 0.3) +
             (High Severity Cases × 0.3)
```

### Risk Levels
- **High Risk** (Score ≥ 2.0)
  - Frequent contamination
  - Multiple diseases
  - Critical severity
  - **Action**: Immediate intervention

- **Medium Risk** (Score 1.0-2.0)
  - Occasional contamination
  - Some diseases
  - Moderate severity
  - **Action**: Regular monitoring

- **Low Risk** (Score < 1.0)
  - Rare contamination
  - Few/no diseases
  - Low severity
  - **Action**: Routine checks

---

## 🆘 Troubleshooting

### Image Upload Issues
- **Problem**: Upload fails
- **Solution**: Check file size (< 10MB), use JPG/PNG

### Analysis Not Working
- **Problem**: No results appear
- **Solution**: Check backend is running (python backend/app.py)

### Map Not Loading
- **Problem**: Blank map
- **Solution**: Click "Refresh Map", check internet connection

### Alert Not Sent
- **Problem**: No notification received
- **Solution**: Check email/phone in NGO registration

---

## 📞 Support

### For Technical Issues
- Check QUICKSTART.md
- Review README.md
- Verify backend is running
- Check browser console for errors

### For Usage Questions
- Refer to this guide
- Check PROJECT_SUMMARY.md
- Review example workflows

### For Deployment
- See DEPLOYMENT.md
- Follow production checklist
- Configure email/SMS properly

---

## 🎓 Training Resources

### For Field Workers
1. How to take water sample photos
2. How to use GPS coordinates
3. How to interpret results
4. When to escalate issues

### For NGO Staff
1. How to respond to alerts
2. How to record actions
3. How to coordinate with others
4. How to track outcomes

### For Administrators
1. How to monitor system health
2. How to analyze patterns
3. How to generate reports
4. How to optimize responses

---

**Remember: This system is a tool to assist decision-making. Always consult healthcare professionals for medical advice and interventions.**

**For emergency health situations, contact local health authorities immediately.**
