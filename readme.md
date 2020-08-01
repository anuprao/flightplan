# Features

## Must have

- Parse XLSX files localfs as input
  
- Node based tasks 
  
  - With dependencies

- Each task has 
  
  - Optional dependencies
   
  - Optional start date, default value is None
  
  - Optional end date, default value is None
  
  - no_of_days, default value is 1
  
  - no_of_hrs, default value is 8
    
  - Optional 'is_critical' flag, default value is false
  
  - Optional 'consider weekend' flag, default value is false
  
  - Optional 'consider holiday' flag, default value is false

- Input validation and preprocessing
  
  - Warn on duplicate ids in single input

  - Auto prefix to task names (helps when combining multiple sources)
   
  - Each input src can define one or more common tracks
  
  - Pull multiple files for input
  
- Generate Gantt related 
  
  - Generate dependency

  - Exclude weekends
    
  - Exclude days from Holiday list
    
  - Specify Milestone dates with dependencies
  
  - Identify node ends 
    
  - Identify node starts
  
- Post Gantt Generation
  
  - Warn on not meeting milestone

- Generate Gantt as SVG or PNG

  - Render tasks
  
    - Typical tasks

        - Without dependencies

        - With dependencies

    - With 'critical' flag
  
    - With 'consideg
  
    - With 'consider holiday' flag

  - Render current date
  
  - Render weekends

  - Render holidays
    
  - Render completed tasks

  - Render milestones
    
  - Render critical tasks
   
  - Render parallel tracks
   
  - Render date range block
  
      - Colour and title on top

      - Useful to highlight sprints, favourable window of opportunity

      - Render legends

## Good to have

- XLS file URL as input
  
- Test 'Leave from work' as task

- Each Day has 6 Hr slots
  
- 1Hr, 2Hr, 4Hr and 8Hr tasks
  
- Warn on less utilization in a day

## Deferred

- Generate sprint suggestions
  
- Generate backlog suggestions
  
- Render connected dependencies








