// red colors, most red to least red
const redList = ['rgb(135, 0, 23)', 'rgb(179, 0, 21)', 'rgb(215, 0, 16)', 'rgb(237, 48, 56)', 'rgb(250, 91, 97)', 'rgb(250, 134, 136)']

// blue colors, least blue to most blue
const blueList = ['rgb(188, 210, 232)', 'rgb(145, 186, 214)', 'rgb(115, 165, 198)', 'rgb(82, 138, 174)', 'rgb(46, 89, 132)', 'rgb(30, 63, 102)']

const combinedList = redList.concat(blueList);

const drColorScale = d3.scale.quantize()
                            .domain([0, 1.0])
                            .range(combinedList);


class ColorInterface {
    constructor() {
    }
    /**
     * Determines the color and opacity
     */
    choose_color(state) {
        const [house_reps, vd] = VOTE_INTERFACE.get_state_values(state);
        if (house_reps < 1.0) {
            return [d3.rgb(0, 0, 0), 1.0]
        }
        return [drColorScale(vd), 1.0];
    }

    /**
     * Used to create the legend
     * Returns domain, range where domain is a list of labels for legend boxes, and range is the corresponding color
     */
    get_legend_domain_range() {
        let domain = [];
        let range = [];
        for (let i = 0; i < 10; i++) {
            let v = 0.1 * i + 0.05;
            if (v < 0.5) {
                domain.push( (1 - (v + 0.05)).toFixed(1).toString() + " < %R < " + (1 - (v - 0.05)).toFixed(1).toString() )
            } else {
                domain.push( (v - 0.05).toFixed(1).toString() + " < %D < " + (v + 0.05).toFixed(1).toString() );
            }
            range.push(drColorScale(v));
        }
        return [ domain, range ];
    }
}
