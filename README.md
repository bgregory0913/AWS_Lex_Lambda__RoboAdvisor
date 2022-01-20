<h3 align="center">About The Project:</h3>
<!-- <p align="center">
  <a href="https://github.com/bgregory0913/AWS_Lex_Lambda__RoboAdvisor/Images">
    <img src="robot.jpg" alt="Robot" align="center">
  </a>
</p> -->


![Robot](https://github.com/bgregory0913/AWS_Lex_Lambda__RoboAdvisor/blob/main/Images/robot.jpg)

# Using AWS Lex and AWS Lambda To Create a RoboAdvisor:
AWS Lex and Lambda can be used to automate just abut any human conversational tasks then securely store and envrypt the conversations. The conversations be done with both text and voice through Lex and can be used, for example, scheduling a doctor appointment, booking a trip, or ordering flowers. AWS provides blueprints for these examples [here](https://us-west-2.console.aws.amazon.com/lex/home?region=us-west-2#bot-create) if you wuold like to learn more.

### Project Overview:
RoboAdvisor services are popping up everywhere and most banks and brokers already use them. They allow investors the opportunity to invest money or receive financial advice without paying to speak to "human" financial advisor.

For this project, I used Lex as the chat interface and Lambda to process and validate the communications between the bot and the customer on the backend.


### RoboAdvisor Inputs
1. Name:
    * Captured so the conversation can be more authentic
2. Age:
    * Captured for validation; retirement portfolios not available for ages 65 and up.
    * Also confirms age is valid (i.e., not 0 or -2)
3. Investment Amount:
    * Validates minimum initial investment of 5,000 USD 
4. Risk Level:
    * Used to determine the best spread of cash between investment options
    
### Outputs
1. Age validation responses
2. Investment amount validation responses
3. Final investment portfolio recommendation

### Built With:
This Lambda code is written in Python (3.7) and connected to the Lex Bot.

* [Python](https://www.python.org/)
* [AWS Lex](https://aws.amazon.com/lex/)
* [AWS Lambda](https://aws.amazon.com/lambda/)


## Contact:
Blake Gregory - [LinkedIn](www.linkedin.com/in/blake-greg) - blake.gregory@tilineum.com
