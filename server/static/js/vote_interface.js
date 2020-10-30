
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
  }


