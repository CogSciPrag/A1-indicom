<template>
  <Experiment title="indicom">

    <InstructionScreen :title="'Welcome'">

      <p>Thank you for taking part in this study.</p> 

      <p>In this experiment, you will play through a <b>small story game</b>.</p> 

      <p>Your task is to read the story carefully and to play through the game. You will be asked to make several choices, such as <b>selecting a topic, choosing a reply to a dialogue and rating the dialogue on a scale</b>. Please answer all questions intuitively - there are no wrong answers.</p>


      <p>You must read all information presented on each page. There will be <b>attention checks</b>, which will test whether you paid attention to the experiment. Please be aware that you cannot go back during the experiment. </p>
    </InstructionScreen>


    <Screen :title="'Instructions'">
      
      <p> You recently moved to a new town and don’t know anyone there apart from your childhood friend John, who has been living in this town for a while already.</p> 

      <p> John offered to help you meet new people, and he is convinced that you will get along with some of his friends, so he is throwing a party for you to speed-date his friends.</p> 

      <p> Now, at this get-together, John introduces you to his friends one after another, telling you about his friends' hobbies and activities they like to do. Since the goal is to find some people to do activities with throughout the week, you have researched a bunch of events and activities happening in the town that you could do together with them.</p>

      <button @click="startTrial(); $magpie.nextScreen()">next</button>

    </Screen>

    <template v-for="(n, currentTrialIndex) in 11">
     <Screen :key="'topic-' + currentTrialIndex" title="At the Party" :name="trial">
      <Slide v-if="currentItems.length === 3">
      
        <p>John: “Meet my friend  {{ shuffledNames[currentTrialIndex].name }}!  {{ shuffledNames[currentTrialIndex].pronoun }} likes {{ currentItems[0].itemName }}, {{ currentItems[1].itemName }}, and {{ currentItems[2].itemName }}.”</p>
        
        <p> <i> Which topic would you like to talk to  {{ shuffledNames[currentTrialIndex].name }}  about? </i> </p>
      
        
       <div class="button-row">
        <button
          v-for="opt in currentItems"
          :key="opt.item"
          @click="selectItem(opt)"
        >
          {{ opt.itemName }}
        </button>
      </div>


      </Slide>
      </Screen>
      
      <Screen :key="'context-' + currentTrialIndex" title="Conversation">
      <Slide v-if="selectedItem">

        <p>You: {{ selectedItem.participantQuestion }} </p>

        <p>  {{ shuffledNames[currentTrialIndex].name }}: {{ selectedItem.contextSentence }}</p>

         <button @click="$magpie.nextScreen()">next</button>

        <div class="comment-container">
              <label class="comment-label">
                Comments (optional):
              </label>

              <textarea
                class="comment-box"
                :placeholder="'If anything was unclear or you have any feedback about this scenario, you can leave it here.'"
                v-model="$magpie.measurements['comment']"
              ></textarea>
            </div>

      </Slide>
      </Screen>


      <Screen 
        v-if="isControlTrial(currentTrialIndex)" 
        :key="'control-' + currentTrialIndex" 
        title="Control Question"
      >
        <Slide v-if="selectedItem">

          <p>
            What did {{ shuffledNames[currentTrialIndex].name }} talk about?
          </p>

          <div class="button-column">
            <button
              v-for="opt in controlOptions"
              :key="opt.text"
              @click="
                controlCorrect = opt.correct;
                $magpie.measurements.controlResponse = opt.text;
                $magpie.measurements.controlCorrect = opt.correct;
                $magpie.saveAndNextScreen()
              "
            >
              {{ opt.text }}
            </button>
          </div>

          <Record :data="{
            trialNum: currentTrialIndex,
            itemID: selectedItem.item,
            itemName: selectedItem.itemName,
            condition: selectedItem.condition,
            controlResponse: $magpie.measurements.controlResponse,
            controlCorrect: $magpie.measurements.controlCorrect
          }" />


        </Slide>
      </Screen>

      <Screen 
        v-if="isControlTrial(currentTrialIndex)" 
        :key="'feedback-' + currentTrialIndex" 
        title="Feedback"
      >
        <Slide>

          <p v-if="controlCorrect === true">
            <b>Great! You got it correct.</b>
          </p>

          <p v-else>
            <b>Incorrect! Please pay more attention to the dialogues from now on.</b>
          </p>

          <button @click="$magpie.nextScreen()">Next</button>

        </Slide>
      </Screen>


      <Screen 
        :key="'rating-' + currentTrialIndex" 
        title="Rating"
      >
      <Slide v-if="selectedItem">

      <p>You: {{ selectedItem.polarQuestion }}</p>

      <p>  {{ shuffledNames[currentTrialIndex].name }}: {{ selectedItem.indirectAnswer }} </p>

      <p class="question-block">
           <i> In this context, does {{ shuffledNames[currentTrialIndex].name }}'s reply mean “no” or “yes”? </i>
        </p>

      <RatingInput
              left="definitely no"
              :response.sync="$magpie.measurements.rating"
              right="definitely yes"
            />

            <p v-if="$magpie.measurements.rating !== undefined &&
                    $magpie.measurements.rating !== null">
              <button @click="$magpie.saveAndNextScreen()">Submit</button>
            </p>

      
        <Record :data="{
          trialNum: currentTrialIndex,
          itemID: selectedItem.item,
          itemName: selectedItem.itemName,
          condition: selectedItem.condition,
          contextType: selectedItem.contextType,
          NAI_type: selectedItem.NAI_type,
          informationStatus: selectedItem['information status'],
          participantQuestion: selectedItem.participantQuestion,
          contextSentence: selectedItem.contextSentence,
          polarQuestion: selectedItem.polarQuestion,
          indirectAnswer: selectedItem.indirectAnswer,
          rating: $magpie.measurements.rating,
          comment: $magpie.measurements['comment'] || null
        }" />


      <div class="comment-container">
              <label class="comment-label">
                Comments (optional):
              </label>

              <textarea
                class="comment-box"
                :placeholder="'If anything was unclear or you have any feedback about this scenario, you can leave it here.'"
                v-model="$magpie.measurements['comment']"
              ></textarea>
            </div>

      </Slide>
      </Screen>


      <Screen 
        :key="'forced_choice-' + currentTrialIndex" 
        title="Choose Reply"
      >
      <Slide v-if="selectedItem">

      <p>You: {{ selectedItem.polarQuestion }}</p>

      <p>  {{ shuffledNames[currentTrialIndex].name }}: {{ selectedItem.indirectAnswer }} </p>

      <p> <i> What do you want to reply to {{ shuffledNames[currentTrialIndex].name }}? </i> </p>

      <div class="button-column">
        <button
          class = "button-selection"
          v-for="opt in currentAnswerOptions"
          :key="opt.answerPolarity"
          @click="selectAnswer(opt); $magpie.saveAndNextScreen()"
        >
          {{ opt.answerOptions }}
        </button>
      </div>

      <Record :data="{
        trialNum: i,
        itemID: selectedItem.item,
        itemName: selectedItem.itemName,
        condition: selectedItem.condition,
        answerChoice: $magpie.measurements.answerChoice,
        answerPolarity: $magpie.measurements.answerPolarity,
        comment: $magpie.measurements['comment'] || null
      }" />

      
      <div class="comment-container">
              <label class="comment-label">
                Comments (optional):
              </label>

              <textarea
                class="comment-box"
                :placeholder="'If anything was unclear or you have any feedback about this scenario, you can leave it here.'"
                v-model="$magpie.measurements['comment']"
              ></textarea>
            </div>


      </Slide>
      </Screen>


      <Screen :key="'continuation-' + currentTrialIndex" title="Continue">
      <Slide> 

      <p> At this point, your friend John interrupts you to introduce you to his next friend. </p> 

      <p> John: “Hey! Come on, let's go meet my next friend!”</p>

      <button @click="startTrial(); $magpie.nextScreen()">Let's go!</button>

      </Slide>
      </Screen>

    </template>
    

    <PostTestScreen />

    <SubmitResultsScreen />
  </Experiment>
</template>


/////////////////////////////////////////////SCRIPT/////////////////////////////////////////

<script>

import main_trials from '../trials/indicom_pilot3_items.csv';
import answerOptions from '../trials/indicom_answerOptions.csv';
import controls from '../trials/indicom_pilot3_controls.csv';

import _ from 'lodash';

//create 8 names for the 8 trials (4 male, 4 female for gender balance) -> these get randomly assigned to the items
const names = [
  { name: "Mary", pronoun: "She", object: "her" },
  { name: "Alex", pronoun: "She", object: "her" },
  { name: "Millie", pronoun: "She", object: "her" },
  { name: "Kate", pronoun: "She", object: "her" },
  { name: "Anna", pronoun: "She", object: "her" },
  { name: "Sarah", pronoun: "She", object: "her" },
  { name: "Karl", pronoun: "He", object: "him" },
  { name: "Bill", pronoun: "He", object: "him" },
  { name: "Bo", pronoun: "He", object: "him" },
  { name: "Tom", pronoun: "He", object: "him" },
  { name: "Andreas", pronoun: "He", object: "him" }
];
const shuffledNames = _.shuffle(names); //shuffle the names into a random order 
const CONTROL_INDICES = [0, 4, 7];


export default { 
  name: 'App', 
  data() {
    return {
      remainingItems: [], // will store 10 unique items and delete them once the participant clicks on an item
      choicesMade: [],  //create empty list to store participants choices of items
      currentItems: [],
      firstMount: true,
      shuffledNames: shuffledNames, //shuffled names
      selectedItem: null,
      conditionOrder: [],
      currentTrialIndex: -1,
      controlCorrect: null

    };
  },

  created() {
    // shuffle condition order once at the start
    this.conditionOrder = _.shuffle([1, 2, 3, 4, 5, 6, 7, 8]);

    // get unique items normally (all 10)
    const seen = new Set();
    this.remainingItems = main_trials.filter(row => {
      if (seen.has(row.item)) return false;
      seen.add(row.item);
      return true;
    });
  },

  computed: {
    // Expose lodash to template code
    _() {
      return _;
    },

    controlOptions() {
      if (!this.selectedItem) return [];

      const options = [
        {
          text: this.selectedItem.correctAnswer,
          correct: true
        },
        {
          text: this.selectedItem.incorrectAnswer,
          correct: false
        }
      ];

      return _.shuffle(options);
    }
  },

  methods: {

     // pick 3 random options from remaining items
    currentOptions() {
      const i = this.currentTrialIndex;

      if (this.isControlTrial(i)) {
        this.currentItems = this.getControlItems(i);
      } else {
        this.currentItems = _.sampleSize(this.remainingItems, 3);
      }
    },
    
    // checks whether a trial is a critical trial or a control
    isControlTrial(i) {
      return CONTROL_INDICES.includes(i);
    },

    //splits the 9 control items into 3 sets of 3
    getControlItems(i) {
      if (i === 0) return controls.slice(0, 3);
      if (i === 4) return controls.slice(3, 6);
      if (i === 7) return controls.slice(6, 9);
    },

    startTrial() {
      this.currentTrialIndex += 1;

      // reset state
      this.currentItems = [];
      this.selectedItem = null;
      this.currentAnswerOptions = [];

      // load items
      this.currentOptions();
    },

    selectItem(item) {
      // store choice
      this.selectedItem = item; 
      this.choicesMade.push(item);

      const i = this.currentTrialIndex;

      if (!this.isControlTrial(i)) {
        const condition = this.conditionOrder.shift();

        this.selectedItem = main_trials.find(
          row => row.item === item.item && parseInt(row.condition) === condition
        );

        // remove chosen item from remaining pool
        this.remainingItems = this.remainingItems.filter(
          (i2) => i2.item !== item.item
        );
      }

      // get answer options (for both control + normal)
      this.currentAnswerOptions = answerOptions.filter(
        row => row.item === item.item
      );

      this.$magpie.nextScreen();
    },


    selectAnswer(opt) {
      this.$magpie.measurements.answerChoice = opt.answerOptions;
      this.$magpie.measurements.answerPolarity = opt.answerPolarity;
    },
  },
};
</script>

/////////////////////////////////////////////STYLE/////////////////////////////////////////


<style>

.button-selection {text-transform:none} 
.context-box {
  display: inline-block;
  background-color: #f0f0f0;  
  padding: 12px 16px;
  padding-left: 30px;
  padding-right: 30px;
  margin-bottom: 20px;
  border-radius: 6px;
}

.question-block {
  margin-top: 10px;   
}

.comment-label {
  display: block;
  font-size: 0.9em;
  color: #666;
  margin-bottom: 6px;
  margin-top: 60px;
}

.comment-box {
  width: 60%;
  min-height: 60px;   
  resize: vertical;    
  padding: 8px 10px;
  font-size: 0.9em;
  border-radius: 6px;
  border: 1px solid #ccc;
  background-color: #fafafa;
}


.button-row {
  display: flex;
  justify-content: center;
}

.button-row button {
  flex: 0 0 auto;
  margin: 0 5px;
  width: auto;
}

.button-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  max-width: 600px;
  margin: 0 auto;
}

.button-column button {
  width: 100%;
  white-space: normal;
  text-align: center;
  padding: 10px 20px;
  margin: 0;
}


</style>