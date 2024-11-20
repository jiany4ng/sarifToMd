# .sarif To .md

Simple python code to convert .sarif into .md ([example](EXAMPLE.md))


# Post Markdown summary as a comment on the pull request using curl
      - name: Comment on pull request
        run: |
          COMMENT_BODY=$(cat sarif_summary.md | jq -R -s '{body: .}')
          curl -s -X POST \
            -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d "$COMMENT_BODY" \
            "https://api.github.com/repos/${{ github.repository }}/issues/${{ github.event.pull_request.number }}/comments"