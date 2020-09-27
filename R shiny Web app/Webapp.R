  # load the required packages
  list.of.packages <- c("ggplot2", "shiny","shinydashboard","plotly")
  new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
  if(length(new.packages)) install.packages(new.packages)
  library(shiny)
  library(shinydashboard)
  library(ggplot2)
  library(plotly)
  
  
  IndData =read.csv('/home/anp/Documents/MSc/Project/Covid19 Dashboard/Covid19 Dataset/Covid19 India Data.csv')
  IndData = data.frame(IndData,header = T)
  
  ui <- dashboardPage(
    dashboardHeader(title = "Covid19 India Cases"),
    dashboardSidebar(collapsed = TRUE,
                     sidebarMenu( menuItem("India", tabName = "india", icon = icon("dashboard"))
                     )
    ),
    dashboardBody(fluidRow(
      valueBoxOutput("value1")
      ,valueBoxOutput("value2")
      ,valueBoxOutput("value3")
    ),  
    box(
      title = "Covid19 Daily Cases : India"
      ,status = "primary"
      ,solidHeader = TRUE 
      ,collapsible = FALSE
      ,plotlyOutput("daily"),
      width="100%", height = "500px"
    )
    ),skin = "red")
  
  
  # create the server functions for the dashboard  
  server <- function(input, output) { 
    #creating the valueBoxOutput content
    output$value1 <- renderValueBox({
      valueBox(
        formatC(IndData$Confirmed[length(IndData$Confirmed)], format="d", big.mark=',')
        ,strong("Total Infected")
        ,icon = icon("stats",lib='glyphicon')
        ,color = "blue")  
    })
    output$value2 <- renderValueBox({ 
      valueBox(
        formatC(IndData$Deaths[length(IndData$Deaths)], format="d", big.mark=',')
        ,strong('Total Deaths')
        ,icon = icon("stats",lib='glyphicon')
        ,color = "red")  
    })
    output$value3 <- renderValueBox({
      valueBox(
        formatC(IndData$Cured[length(IndData$Cured)], format="d", big.mark=',')
        ,strong('Total Recovered')
        ,icon = icon("heart-empty",lib='glyphicon')
        ,color = "green")   
    })
    #creating the plotOutput content
    output$daily <- renderPlotly({
      #importing data
      IndData = data.frame(read.csv('/home/anp/Documents/MSc/Project/Covid19 Dashboard/Covid19 Dataset/Covid19 India Data.csv'))
      #LiveData = read.csv
      ggplot(IndData, aes(x=as.Date(Date))) + 
        geom_area(aes(y= Confirmed, fill="Number.of.Cases")) + 
        geom_area(aes(y= Deaths, fill="Number.of.Deaths")) +
        geom_area(aes(y= Cured, fill="Number.of.Cured")) + 
        labs(title="Covid19 India Daily Cases", x = "Date",
             caption=" Data Source: Ministry of Health and Family Welfare Government of India", 
             y="Daily Cases") +  # title and caption # change to monthly ticks and labels
        scale_fill_manual(name="", 
                          values = c("Number.of.Cases"="steelblue", "Number.of.Deaths"="firebrick1","Number.of.Cured"="springgreen3")) +  # line color
        theme(panel.grid.minor = element_blank())
      
      
    })
  }
  
  
  
  #run/call the shiny app
  shinyApp(ui, server)