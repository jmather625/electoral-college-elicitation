// predeclared: VOTE_INTERFACE, MAP_DATA
// format of tweetData: DISTRICT -> PARTY -> CANDIDATE -> POLARITY -> [total_likes, num_tweets, avg_sentiment, tweet]
// tweet keys: likes, username, tweet_text, tweet_date, date_descriptor
// there are also 'combined' values at the CANDIDATE and PARTY level

// define a function on strings to turn "COOK COUNTY" into "Cook County"
String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};

const reset = function() {
    opacity_dict = null;
}

// declare variables
let COLOR_INTERFACE = new ColorInterface();

// SVG
const width = 1200;
const height = 700;

const projection = d3.geo.mercator()
                        .scale(600)
                        .center([-99, 39])
                        .translate([width / 2, height / 2 + 25]);

const path = d3.geo.path()
                    .projection(projection);

const svg = d3.select('svg')
                .attr('width', width)
                .attr('height', height);

const legendLayer = svg.append('g')
                        .classed('legend-layer', true)
                        .attr('transform', "translate(" + (-width/2) + "," + (100) + ")");

const mapLayer = svg.append('g')
                    .classed('map-layer', true);

// const textLayer = svg.append('g')
//                     .classed('text-layer', true)
//                     .attr("x", (width / 2))
//                     .attr("y", 60)
//                     .attr("text-anchor", "middle")
//                     .style("font-size", "30px")
//                     .style("font-family", "Arial")
//                     .text("huzzaaa");

// const textLabels = mapLayer.selectAll('path')
//                             .data(features)
//                             .enter().append('path')
//                             .attr("x", function(d) {return 300})
//                             .attr("y", function(d) {return 300})
//                             .text("whaddup");

const hover_div = d3.select("body").append("div")
                                    .attr("class", "hover-text")
                                    .style("opacity", 0);


const construct_hover_text = function(state) {
    /** 
     * FORMAT:
     * TODO
    */
   return "wassup";
}


// functions
const displayBaseMap = function () {
    // this is a global declared in the html
    const features = MAP_DATA.features;

    // title
    mapLayer.append("text")
            .classed("text", true)
            .attr("x", (width / 2))
            .attr("y", 60)
            .attr("text-anchor", "middle")
            .style("font-size", "30px")
            .style("font-family", "Arial")
            .text("Illinois Counties");


    mapLayer.selectAll('path')
                .data(features)
                .enter().append('path')
                .attr('d', path)
                .attr('vector-effect', 'non-scaling-stroke')
                .attr("id", function(d, i) {return "path_" + i.toString()})
                //Our new hover effects
                .on('mouseover', function (d, i) {
                    d3.select(this).transition()
                        .duration('50')
                        .attr('opacity', '.85');
                    hover_div.transition()
                        .duration(50)
                        .style("opacity", 1);
                    const text = construct_hover_text(d.properties['STATE_NAME']);
                    d.properties['OLD_OPACITY'] = $(this).css("opacity");
                    if (text !== null) {
                        hover_div.html(text)
                                    .style("left", (d3.event.pageX + 10) + "px")
                                    .style("top", (d3.event.pageY - 15) + "px");
                    }
                    else {
                        hover_div.transition()
                                    .duration('50')
                                    .style("opacity", 0);
                    }
            })
            .on('mouseout', function (d, i) {
                    d3.select(this).transition()
                        .duration('50')
                        .attr('opacity', d.properties['OLD_OPACITY']);
                    hover_div.transition()
                        .duration('50')
                        .style("opacity", 0);
            });

    for (var i = 0; i < 50; i++) {
        var state = features[i].properties['STATE_NAME'];
        console.log(state);
        // Add a text label.
        var text = svg.append("text")
            // .attr("dx", 5)
            // .attr("dy", 5);

        text.append("textPath")
        .attr("stroke","black")
        .attr("xlink:href","#path_" + i.toString())
        .text( VOTE_INTERFACE.get_state_values(state)[0] );
    }

    console.log("done rendering base map!");
}

const colorMap = function() {
    mapLayer.selectAll('path')
        .style('fill', function (d) {
            const [color, opacity] = COLOR_INTERFACE.choose_color(d.properties['STATE_NAME']);
            d3.select(this).transition()
                            .duration('50')
                            .attr('opacity', opacity);
            return color;
        });
}

const createLegend = function() {
    const [domain, range] = COLOR_INTERFACE.get_legend_domain_range();
    domain.push('No data');
    range.push(d3.rgb(0, 0, 0)); // black

    const quant = d3.scale.ordinal()
                        .domain(domain)
                        .range(range);
        
    legendLayer.select('g').remove();
    const legend = legendLayer.append("g")
                            .attr("class", "legend")
                            .attr("transform", "translate(" + width * 6/9 + "," + height / 3 + ")")
                            .style('font-family', 'Garamond')
                            .style('font-size', '16')
                            .style('position', 'absolute');

    const legendQuant = d3.legend.color()
                                    // .title("Legend")
                                    .labelFormat(d3.format('.0f'))
                                    .scale(quant);

    legend.call(legendQuant);
}

displayBaseMap();
colorMap();
createLegend();


