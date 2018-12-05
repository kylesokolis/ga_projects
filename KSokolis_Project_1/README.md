## Problem Statement¶
Like Illinois, all states should be required to offer at least one of the two standard college entrance exams so all students upon exiting high school have nothing test-wise standing in their way in their pursuit of a secondary education.

---
---

## Executive Summary
### Contents:
- [2017 Data Import and Cleaning](#Data-Import-and-Cleaning)
- [2018 Data Import and Cleaning](#2018-Data-Import-and-Cleaning)
- [Exploratory Data Analysis](#Exploratory-Data-Analysis)
- [Data Visualization](#Visualize-the-data)
- [Descriptive and Inferential Statistics](#Descriptive-and-Inferential-Statistics)
- [Outside Research](#Outside-Research)
- [Conclusions and Recommendations](#Conclusions-and-Recommendations)

---
---

|**Feature**|**Type**|**Dataset**|**Description**|
|---|---|---|---|
|act      | dictionary |act_2017 | ACT averages from all 50 states.|
|state_2017_act|object|act_2017|The state reporting ACT scores|
|participation_percent_2017_act|integer|act_2017|Percentage of participation in the ACT from schools in the state listed.|
|english_2017_act|float|act_2017|Average scores from the English portion of the ACT.|
|math__2017_act|float|act_2017|Average scores from the Math portion of the ACT.|
|reading_2017_act|float|act_2017|Average scores from the Reading portion of the ACT.|
|science_2017_act|float|act_2017|Average scores from the Science portion of the ACT.|
|composite_2017_act|float|act_2017|Average composite score for the ACT.|

---
---

|**Feature**|**Type**|**Dataset**|**Description**|
|---|---|---|---|
|sat      | dictionary |sat_2017 | SAT averages from all 50 states.|
|state_2017_sat|object|sat_2017|The state reporting SAT scores|
|participation_percent_2017_sat|integer|sat_2017|Percentage of participation in the SAT from schools in the state listed.|
|reading_and_writing_2017_sat|integer|sat_2017|Average scores from the Evidence-Based Reading and Writing portion of the SAT.|
|math__2017_sat|integer|sat_2017|Average scores from the Math portion of the SAT.|
|total_2017_sat|integer|sat_2017|Average Total score for the SAT.|