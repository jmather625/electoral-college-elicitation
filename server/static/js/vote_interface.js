
class VoteInterface {
    constructor(voteData) {
      this.voteData = voteData;
    }

    set_data(voteData) {
        this.voteData = voteData;
    }

    get_state_values(state) {
        /**
         * Returns [number of house reps, fraction voting democrat]
         */
        state = state.toUpperCase();
        const state_data = this.voteData[state];
        if (state_data == null) {
          return [0.0, 0.0];
        }
        return [ state_data["h"], state_data["dv"] ];
    }

    get_aggregate_statistics() {
      /**
       * Returns [total popular %D, total votes D, total votes R, num blue states, num red states]
       */
      let total_votes_d = 0;
      let total_votes_r = 0;
      let num_blue = 0;
      let num_red = 0;
      let pop_blue = 0;
      let pop_red = 0;
      for (var state in this.voteData) {
        let h = this.voteData[state]["h"];
        let dv = this.voteData[state]["dv"];
        total_votes_d += h * HOUSE_REP_TO_POP * dv;
        total_votes_r += h * HOUSE_REP_TO_POP * (1 - dv);
        if (dv > 0.5) {
          num_blue += 1;
          pop_blue += h * HOUSE_REP_TO_POP;
        } else {
          num_red += 1;
          pop_red += h * HOUSE_REP_TO_POP;
        }
      }

      const total_pop_d = total_votes_d / (total_votes_d + total_votes_r);
      return [total_pop_d, total_votes_d.toFixed(0), total_votes_r.toFixed(0), num_blue, num_red, pop_blue, pop_red];
    }
  }


