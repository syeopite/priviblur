"""Extensions to npf-renderer to allow asynchronous code and some other custom styling"""

import dominate
import npf_renderer

from .helpers import url_handler


class NPFParser(npf_renderer.parse.Parser):
    def __init__(self, content, poll_callback=None):
        super().__init__(content, poll_callback)

    async def _parse_poll_block(self):
        poll_id = self.current.get("clientId") or self.current.get("client_id")
        if poll_id is None:
            raise ValueError("Invalid poll ID")

        question = self.current["question"]

        answers = {}
        for raw_ans in self.current["answers"]:
            answer_id = raw_ans.get("clientId") or raw_ans.get("client_id")
            answer_text = raw_ans.get("answerText") or raw_ans.get("answer_text")

            if answer_id is None or answer_text is None:
                raise ValueError("Invalid poll answer")

            answers[answer_id] = answer_text

        votes = None
        total_votes = None

        if self.poll_result_callback:
            callback_response = await self.poll_result_callback(poll_id)

            #{answer_id: vote_count}
            raw_results = callback_response["results"].items()
            processed_results = sorted(raw_results, key=lambda item: -item[1])

            votes_dict = {}
            total_votes = 0

            for index, results in enumerate(processed_results):
                vote_count = results[1]
                total_votes += vote_count

                if index == 0:
                    votes_dict[results[0]] = npf_renderer.objects.poll_block.PollResult(is_winner=True, vote_count=vote_count)
                else:
                    votes_dict[results[0]] = npf_renderer.objects.poll_block.PollResult(is_winner=False, vote_count=vote_count)

            votes = npf_renderer.objects.poll_block.PollResults(
                timestamp=callback_response["timestamp"],
                results=votes_dict
            )

        creation_timestamp = self.current["timestamp"]
        expires_after = self.current["settings"]["expireAfter"]

        return npf_renderer.objects.poll_block.PollBlock(
            poll_id=poll_id,
            question=question,
            answers=answers,

            creation_timestamp=int(creation_timestamp),
            expires_after=int(expires_after),

            votes=votes,
            total_votes=total_votes,
        )

    async def __parse_block(self):
        """Parses a content block and appends the result to self.parsed_result

        Works by routing specific content types to corresponding parse methods
        """

        match self.current["type"]:
            case "text":
                block = self._parse_text()
            case "image":
                block = self._parse_image_block()
            case "link":
                block = self._parse_link_block()
            case "audio":
                block = self._parse_audio_block()
            case "video":
                block = self._parse_video_block()
            case "poll":
                block = await self._parse_poll_block()
            case _:
                block = unsupported.Unsupported(self.current["type"])

        self.parsed_result.append(block)

    async def parse(self):
        """Begins the parsing chain and returns the final list of parsed objects"""
        while self.next():
            await self.__parse_block()

        return self.parsed_result


async def format_npf(contents, layouts=None, *, poll_callback=None):
    try:
        contents = await NPFParser(contents, poll_callback=poll_callback).parse()
        if layouts:
            layouts = npf_renderer.parse.LayoutParser(layouts).parse()

        contains_render_errors = False

        formatted = npf_renderer.format.Formatter(contents, layouts, url_handler=url_handler,
            forbid_external_iframes=True,
        ).format()

    except npf_renderer.exceptions.RenderErrorDisclaimerError as e:
        contains_render_errors = True
        formatted = e.rendered_result
        assert formatted is not None
    except Exception as e:

        formatted = dominate.tags.div(cls="post-body has-error")
        contains_render_errors = True

    return contains_render_errors, formatted.render(pretty=False)
