# Features

## Must have

- Parse XLSX files localfs as input
  
- Node based tasks 
  
  - With dependencies

  - Warn of circular dependencies

- Each task has 
  
  - Optional dependencies
   
  - Optional start_date, default value is None
  
  - Optional end_date, default value is None
  
  - no_of_days, default value is 1
  
  - no_of_hrs, default value is 8
    
  - Optional 'is_critical' flag, default value is false
  
  - Optional 'consider_weekend' flag, default value is false
  
  - Optional 'consider_holiday' flag, default value is false
  
  - Optional 'is_complete' flag, default value is false

- Input validation and preprocessing
  
  - Warn on duplicate ids in single input

  - Auto prefix to task names (helps when combining multiple sources)
   
  - Each input src can define one or more common tracks
  
  - Pull multiple files for input
  
- Generate Gantt related 
  
  - Generate dependency chart with tasks and start date

  - Exclude weekends
    
  - Exclude days from Holiday list
    
  - Specify Milestone dates with dependencies
  
  - Identify node ends 
    
  - Identify node starts
  
- Post Gantt Generation
  
  - Warn on not meeting milestone

- Generate Gantt as SVG or PNG

  - Render tasks

    - Without dependencies, colour: yellow

    - With dependencies, colour: light yellow

    - With 'critical' flag, colour: red boundary
  
    - With 'consider weekend' flag, colour: orange1 boundary
  
    - With 'consider holiday' flag, colour: orange2 boundary

    - With 'is_complete' flag, colour: blue

  - Render current dateline, colour: red
  
  - Render weekends, colour: faint orange1

  - Render holidays, colour: faint orange2

  - Render milestones, colour: red
   
  - Render parallel tracks, colour:alternating background of white and light grey
   
  - Render custom date range block

      - Useful to highlight sprints, favourable window of opportunity

## Good to have

- XLS file URL as input
  
- Test 'Leave from work' as task

- Each Day has 6 Hr slots
  
- 1Hr, 2Hr, 4Hr and 8Hr tasks
  
- Warn on less utilization in a day

## Deferred

- Generate sprint suggestions
  
- Generate backlog suggestions
  
- Render custom date range block

    - Colour and title on top

    - Render legends
 
- Render connected dependencies








