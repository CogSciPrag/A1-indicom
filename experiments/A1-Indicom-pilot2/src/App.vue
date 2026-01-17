<template>
  <Experiment title="indicom">
    <InstructionScreen :title="'Welcome'">
      <p>Thank you for taking part in this study.</p> 

      <p>In this experiment, you will be shown small fictional dialogues each consisting of a question and an answer, and a context in which the dialogue takes place.</p>

      <p>Your task is to read the scenario carefully and to rate whether you think the answer given to the question means “no” or “yes” on a scale from 1 (“definitely no”) to 7 (“definitely yes”), given the context sentence.</p> 

      <p>You must read all information presented with each scenario. There will be attention checks, which ask you to give a specific rating. </p>
    </InstructionScreen>

    <template v-for="(triple, tIndex) in sampledTriples">
      <template v-for="(trial, i) in triple">
        <Screen title="Dialogue"
                :key="'t'+tIndex+'_i'+i" 
                :progress="(tIndex * 4 + i + 1) / totalScreens">
          <Slide>
            

            <p class="context-box">    
            {{ trial.speaker1 }}:  <b> {{ trial.polarquestion }} </b> <br>
            {{ trial.speaker2 }}:  <b> {{ trial.indirectanswer }} </b> </p>

            <p class="context-box"> This exchange takes place in a context where {{ trial.speaker1 }} and {{ trial.speaker2 }} share the following piece of knowledge: <br>
            <b> {{ trial.contextsentence }} </b></p>

            <p class="question-block">
            In this context, does {{ trial.speaker2 }}’s reply mean “no” or “yes”?
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

            <Record
              :data="{
                trialType: trial.trialType,
                key: 'trial_' + tIndex + '_' + i,
                itemID: trial.Item,
                contextType: trial['Context Type'],
                rating: $magpie.measurements.rating,
                comment: $magpie.measurements['comment'] || null,
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

  trials.forEach(t => (t.trialType = 'main'));

  //cycle so each triple gets a different attention check
  const ac = cleanAttention[tIndex % cleanAttention.length];
  
  //mark trial type as attention check
  ac.trialType = 'attention'; 

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
      screensPerTriple: 4,
      attentionChecks: attentionChecks
    };
  },
  
  computed: {
    // Expose lodash to template code
    _() {
      return _;
    },

    totalScreens() {
      return this.sampledTriples.length * this.screensPerTriple;
    }
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
  min-height: 60px;   /* bigger box */
  resize: vertical;    /* allow expansion but not horizontal chaos */
  padding: 8px 10px;
  font-size: 0.9em;
  border-radius: 6px;
  border: 1px solid #ccc;
  background-color: #fafafa;
}

</style>