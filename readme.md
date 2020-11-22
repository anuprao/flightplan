# Features

## Must have

-[o]- Parse XLSX files localfs as input

  -[*]- Read XLS files from localfs

  -[*]- Read and populate - General

    -[*]- Holiday Plan

    -[*]- Event Plan

    -[*]- Milestone Plan

    -[*]- Project Tracks

    -[*]- Work Hours

  -[*]- Read and populate - Member Data

    -[*]- Leave Plan

    -[*]- Work Hours

  -[*]- Read and populate - Tasks 

    -[*]- task name

    -[*]- task desc

    -[*]- task depends on

    -[*]- start_date

    -[*]- num_man_hours

    -[*]- members

    -[*]- is_critical

    -[*]- is_complete

    -[*]- consider_weekend

    -[*]- consider_holiday

  -[o]- Read XLS file from URL
  
-[✓]- Node based tasks 
  
  -[✓]- With dependencies

  -[✓]- Warn of circular dependencies

-[o]- Each task has 
  
  -[✓]- Optional dependencies
   
  -[✓]- Optional start_date, default value is None
  
  -[✓]- num_man_hrs, default value is 8

  -[o]- Optional end_date, default value is None
    
  -[✓]- Optional 'is_critical' flag, default value is false
  
  -[o]- Optional 'consider_weekend' flag, default value is false
  
  -[o]- Optional 'consider_holiday' flag, default value is false
  
  -[✓]- Optional 'is_complete' flag, default value is false

-[o]- Input validation and preprocessing
  
  -[*]- Warn on duplicate ids in single input

  -[*]- Auto prefix to task names (helps when combining multiple sources)
  
  -[-]- Pull multiple files for input
  
-[o]- Generate Gantt related 
  
  -[✓]- Generate dependency chart with tasks and start date

  -[✓]- Exclude weekends
    
  -[✓]- Exclude days from Holiday list
    
  -[o]- Specify Milestone dates with dependencies
  
  -[✓]- Identify node ends 
    
  -[✓]- Identify node starts
  
-[o]- Post Gantt Generation
  
  -[o]- Warn on not meeting milestone

-[o]- Generate Gantt as SVG or PNG

  -[✓]- Render tasks

    -[✓]- Without dependencies, colour: yellow

    -[✓]- With dependencies, colour: light yellow

    -[✓]- With 'critical' flag, colour: red boundary
  
    -[✓]- With 'consider weekend' flag, colour: orange1 boundary
  
    -[✓]- With 'consider holiday' flag, colour: orange2 boundary

    -[✓]- With 'is_complete' flag, colour: blue

  -[✓]- Render current dateline, colour: red
  
  -[✓]- Render weekends, colour: faint orange1

  -[✓]- Render holidays, colour: faint orange2

  -[✓]- Render milestones, colour: red
   
  -[✓]- Render parallel tracks, colour:alternating background of white and light grey
   
  -[o]- Render custom date range block

      -[o]- Useful to highlight sprints, favourable window of opportunity

## Good to have

-[o]- XLS file URL as input
  
-[✓]- Test 'Leave from work' as task

-[✓]- Each Day has 8 Hr slots
  
-[✓]- 1Hr, 2Hr, 4Hr and 8Hr tasks
  
-[o]- Warn on less utilization in a day

## Deferred

-[o]- Generate sprint suggestions
  
-[o]- Generate backlog suggestions
  
-[*]- Render custom date range block

    -[✓]- Colour and title on top

    -[*]- Render legends
 
-[✓]- Render connected dependencies








