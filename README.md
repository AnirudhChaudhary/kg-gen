# kg-gen

# Anirudh Chaudhary 
This project will be able to create a concept graph from course material or any piece of material that is provided as input.

The goal of this is for instructors to be able to pass in their course content and be able to see what connections are formed over the course of a chapter or book. Being able to form connections from one end of the book to the other is helpful for making stronger connections to the material.

With the condensed version of the course content, the next step will be to generate practice problems that involve different concepts that an instructor wants to be tested. 

# Timeline
1. Generate condensed versions of course content for a chapter
    - Explore generator - breaker - summarizer architecture for synthesizing, evaluating, and condensing the material. The idea behind this is that the synthesizer is just responsible for creating the content while the breaker is trying to patch up holes in the content. The summarizer comes in and condenses everything to remove the fluff.
    - Output Format:
        {
            topic: <string>
            descr: <string>
            related_topics: List[<string>]
        }
2. Using the generated responses from the chapter, sync them across chapters to analyze dependencies
