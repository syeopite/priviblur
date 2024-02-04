"use strict";

function requestPollResults(poll_element, pollId) {
    return new Promise(function (resolve, reject) {
        let post = poll_element.closest(".post");
        const blogName = post.getElementsByClassName("blog-name")[0].innerHTML;
        const postId = post.dataset.postId;

        const pollResultsFetch = fetch(`/api/v1/poll/${blogName}/${postId}/${pollId}/results`);

        pollResultsFetch.then((results) => {
            return results.json();
        }).then((parsed_results) => {
            return resolve(parsed_results);
        });
    })
}

function fill_poll_results(poll_element, results) {
    const sorted_poll_results = Object.entries(results.response.results).sort((a,b) => (a[1]-b[1])).reverse();

    // Find total votes first
    let total_votes = 0;
    for (let votes of sorted_poll_results) {
        total_votes += votes[1];
    };

    // Create mapping of answer-id to answer choice element
    const answerIdToChoiceElement = {}
    const pollBody = poll_element.getElementsByClassName("poll-body")[0]

    for (let choiceElement of pollBody.children) {
        answerIdToChoiceElement[choiceElement.dataset.answerId] = choiceElement
    }

    for (let i = 0; i < sorted_poll_results.length; ++i) {
        const [answer_id, answer_votes] = sorted_poll_results[i];
        const choiceElement = answerIdToChoiceElement[answer_id]

        const numericalVoteProportion = answer_votes/total_votes

        const voteProportionElement = document.createElement("span");
        voteProportionElement.classList.add("vote-proportion");
        voteProportionElement["style"] = `width: ${((numericalVoteProportion) * 100).toFixed(3)}%;`;

        const voteCountElement = document.createElement("span");
        voteCountElement.classList.add("vote-count");

        // A greater rounding precision is needed here
        if ((Math.round((numericalVoteProportion) * 10000)/10000) > 0.001) {
            voteCountElement.innerHTML = new Intl.NumberFormat("en-US", {style: "percent", maximumSignificantDigits: 3}).format(Math.round((numericalVoteProportion) * 1000)/1000);
        } else {
            voteCountElement.innerHTML = "< 0.1%";
        }

        if (i == 0) {
            choiceElement.classList.add("poll-winner");
        }

        choiceElement.appendChild(voteProportionElement);
        choiceElement.appendChild(voteCountElement);
    }

    const totalVotesElement = document.createElement("p")

    if (poll_element.classList.contains("expired")) {
        totalVotesElement.innerHTML = `Final result from ${total_votes} votes`
    } else {
        totalVotesElement.innerHTML = `${total_votes} votes`
    }

    const poll_footer = poll_element.getElementsByTagName("footer")
    poll_footer[0].insertBefore(totalVotesElement, poll_footer[0].firstChild)
}

const pollBlocks = document.getElementsByClassName("poll-block");


function populate_polls() {
    for (let poll of pollBlocks) {
        if (poll.classList.contains("populated")) {
            continue;
        }

        requestPollResults(poll, poll.dataset.pollId).then((answers) => {fill_poll_results(poll, answers)})
    }    
};

// TODO lazy load polls
populate_polls();
