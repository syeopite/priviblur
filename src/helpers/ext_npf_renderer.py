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

        creation_timestamp = self.current["timestamp"]
        expires_after = self.current["settings"]["expireAfter"]

        votes = None
        total_votes = None

        if self.poll_result_callback:
            callback_response = await self.poll_result_callback(poll_id, creation_timestamp + expires_after)

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


class NPFFormatter(npf_renderer.format.Formatter):
    def __init__(self, content, layout=None, blog_name=None, post_id=None, *, url_handler=None, forbid_external_iframes=False):
        super().__init__(content, layout, url_handler=url_handler, forbid_external_iframes=forbid_external_iframes)

        # We store the blog and post ID as to be able to render a link to
        # fetch poll results for JS disabled users
        self.blog_name = blog_name
        self.post_id = post_id

    def _format_poll(self, block):
        poll_html = super()._format_poll(block)
        poll_html["data-poll-id"] = block.poll_id

        poll_body = poll_html[1]
        for index, answer_id in enumerate(block.answers.keys()):
            poll_body[index]["data-answer-id"] = answer_id

        if (self.blog_name and self.post_id) and not block.votes:
            poll_footer = poll_html[2]
            no_script_fallback = dominate.tags.noscript(
                    dominate.tags.a(
                        "See Results",
                        href=f"/{self.blog_name}/{self.post_id}?fetch_polls=true",
                        cls="toggle-poll-results"
                    )
                )

            poll_footer.children.insert(0, no_script_fallback)

        return poll_html


async def format_npf(contents, layouts=None, blog_name=None, post_id=None,*, poll_callback=None):
    """Wrapper around npf_renderer.format_npf for extra functionalities

    - Replaces internal Parser and Formatter with the modified variants above
    - Accepts extra arguments to add additional details to formatted results
    - Automatically sets Priviblur-specific rendering arguments

    Arguments (new):
        blog_name:
            Name of the blog the post comes from. This is used to render links to the parent post
        post_id:
            Unique ID of the post. This is used to render links to the parent post
    """
    try:
        contents = await NPFParser(contents, poll_callback=poll_callback).parse()
        if layouts:
            layouts = npf_renderer.parse.LayoutParser(layouts).parse()

        contains_render_errors = False

        formatted = NPFFormatter(
            contents, layouts,
            blog_name=blog_name,
            post_id=post_id,
            url_handler=url_handler,
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
