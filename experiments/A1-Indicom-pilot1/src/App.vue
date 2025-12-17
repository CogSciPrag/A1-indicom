<template>
  <Experiment title="indicom">
    <InstructionScreen :title="'Welcome'">
      <p>Thank you for taking part in my study.</p> 

      <p>In this experiment, you will be shown small fictional dialogues each consisting of a context sentence, a question and an answer.</p>

      <p>Your task is to read the scenario carefully and to rate whether you think the answer means „no“ or „yes“ on a scale from 1 („definitely no“) to 7 („definitely yes“).</p> 
    </InstructionScreen>

    <template v-for="(triple, tIndex) in sampledTriples">
      <template v-for="(trial, i) in triple">
        <Screen :key="'t'+tIndex+'_i'+i">
          <Slide>
            
            <div class="context-box">
              <p>{{ trial.contextsentence }}</p>
            </div>

                
            <p><b>{{ trial.speaker1 }}:</b> {{ trial.polarquestion }}</p>
            <p><b>{{ trial.speaker2 }}:</b> {{ trial.indirectanswer }}</p>

            <p class="question-block">
              Does {{ trial.speaker2 }}’s reply mean “no” or “yes”?
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

            <Record
              :data="{
                trialType: 'main',
                key: 'trial_' + tIndex + '_' + i,
                itemID: trial.Item,
                contextType: trial['Context Type'],
                rating: $magpie.measurements.rating,
                speaker1: trial.speaker1,
                speaker2: trial.speaker2
              }"
            />


          </Slide>
        </Screen>
      </template>
    </template>

    <PostTestScreen />

    <SubmitResultsScreen />
  </Experiment>
</template>

<script>

import main_trials from '../trials/indicom_items.csv'
import attentionChecks from '../trials/attention_checks.csv';

import _ from 'lodash';

//clean csv 
const cleanMainTrials = main_trials.map(row => ({
  ...row,
  Item: Number(row["Item"]),
  "Context Type": row["Context Type"].trim().toLowerCase()
}));

const cleanAttention = attentionChecks.map(row => ({
  ...row,
  "Context Type": row["Context Type"].trim().toLowerCase()
}));

const conditions = ["positive", "negative", "neutral"];

//create triples
const itemIDs = _.range(1, 31);
const sampledIDs = _.sampleSize(itemIDs, 9);
const triples = _.chunk(sampledIDs, 3);

//build the sampled triples
const sampledTriples = triples.map((triple, tIndex) => {
  const shuffledConditions = _.shuffle(conditions);

  const trials = triple.map((id, i) => {
    const condition = shuffledConditions[i];

    const row = cleanMainTrials.find(
      item =>
        item.Item === id &&
        item["Context Type"] === condition
    );

    return row || null; // placeholder so array length stays stable
  });

  //cycle so each triple gets a different attention check
  const ac = cleanAttention[tIndex % cleanAttention.length];
  
  //insert the attention check at the end of the triple
  trials.push(ac);

  return trials;
});

console.log("RESULT sampledTriples:", sampledTriples);




export default { 
  name: 'App', 
  data() {
    return {
      sampledIDs: sampledIDs,
      triples: triples,
      sampledTriples: sampledTriples,
      attentionChecks: attentionChecks
    };
  },
  
  computed: {
    // Expose lodash to template code
    _() {
      return _;
    },
  }
  
};
</script>

<style>
.context-box {
  display: inline-block;
  background-color: #f0f0f0;  
  padding: 12px 16px;
  padding-left: 30px;
  padding-right: 30px;
  margin-bottom: 20px;
  border-radius: 6px;
  font-style: italic;
}

.question-block {
  margin-top: 30px;   
}
</style>