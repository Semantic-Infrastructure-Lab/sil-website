# Contributing to SIL

**Thank you for your interest in contributing to the Semantic Infrastructure Lab!**

The Semantic Infrastructure Lab (SIL) is building the foundational semantic substrate for intelligent systems. We welcome contributions from researchers, developers, and domain experts who share our vision of explicit semantic infrastructure.

---

## Ways to Contribute

### 1. Documentation Improvements 📝

Help make SIL's ideas more accessible:
- Fix typos, broken links, or unclear explanations
- Add examples or tutorials
- Improve diagrams and visualizations
- Translate documentation

**How:** Submit a pull request to [sil-website](https://github.com/semantic-infrastructure-lab/SIL) with your changes.

---

### 2. Research Feedback 🔬

Engage with SIL's research:
- Provide feedback on published research (RAG manifold transport, agent-help standard)
- Share related work or relevant papers
- Propose connections to existing research
- Identify gaps or limitations

**How:** Open an issue with the `research` label or join discussions in [GitHub Discussions](https://github.com/semantic-infrastructure-lab/SIL/discussions).

---

### 3. Tool Development 🛠️

Build on SIL's production tools:
- Contribute to [reveal](https://github.com/semantic-infrastructure-lab/reveal) - Code structure exploration
- Report bugs or request features for existing tools
- Build adapters or integrations
- Implement the [agent-help standard](/docs/agent-help-standard) in your CLI tools

**How:** Each project has its own CONTRIBUTING.md with specific guidelines. See the [Project Index](/projects) for links.

---

### 4. Standards Proposals (RFCs) 💡

**SIL uses an RFC (Request for Comments) process for proposing new standards, patterns, or significant changes.**

#### When to Use RFCs:
- Proposing a new semantic standard or protocol
- Major architectural changes to existing systems
- New additions to the Semantic OS specification
- Standards that affect multiple SIL projects

#### RFC Process:

**1. Discussion Phase** (1-2 weeks)
- Open a GitHub Discussion with `[RFC]` prefix
- Describe the problem and proposed solution
- Gather initial feedback from community
- Refine the proposal based on discussion

**2. Formal Proposal** (Draft RFC)
- Create a markdown document with:
  - **Problem Statement:** What gap or issue does this address?
  - **Proposed Solution:** Technical specification
  - **Design Rationale:** Why this approach?
  - **Alternatives Considered:** What else was evaluated?
  - **Implementation Plan:** How would this be realized?
  - **Success Criteria:** How do we know it works?
- Submit as a pull request to `docs/rfcs/`

**3. Review & Refinement** (2-4 weeks)
- Community reviews and provides feedback
- Author addresses concerns and iterates
- SIL core team provides technical guidance
- Consensus building through discussion

**4. Decision**
- **Accepted:** RFC is merged, implementation can proceed
- **Deferred:** Good idea, wrong timing - revisit later
- **Rejected:** Doesn't align with SIL principles or vision

**5. Implementation**
- Accepted RFCs are tracked for implementation
- Implementation can be done by RFC author or community
- Progress tracked via GitHub issues/projects

#### RFC Evaluation Criteria:
RFCs are evaluated against **SIL's 14 principles:**
- ✅ Clarity - Is structure visible?
- ✅ Simplicity - Is complexity minimized?
- ✅ Composability - Does it integrate cleanly?
- ✅ Correctness - Is behavior well-defined?
- ✅ Verifiability - Can claims be validated?
- ✅ Semantic Primacy - Does meaning come first?
- ✅ Human + Machine - Readable by both?
- ... [See full principles](/docs/sil-principles)

**Example Past RFCs:**
- Agent-Help Standard (Status: Accepted, Implemented in Reveal v0.13.0+)
- Progressive Disclosure Pattern (Status: Accepted, Production validated)

---

## Community Guidelines

### Code of Conduct

**SIL is committed to a harassment-free, inclusive environment.**

Expected behavior:
- ✅ Be respectful and constructive in feedback
- ✅ Welcome diverse perspectives and backgrounds
- ✅ Focus on ideas and technical merit
- ✅ Assume good faith in discussions
- ✅ Give credit where credit is due

Unacceptable behavior:
- ❌ Personal attacks or ad hominem arguments
- ❌ Harassment, intimidation, or discrimination
- ❌ Trolling, inflammatory comments, or derailing discussions
- ❌ Publishing others' private information
- ❌ Any conduct that creates an unsafe environment

**Reporting:** If you experience or witness unacceptable behavior, contact [conduct@semanticinfrastructurelab.org](mailto:conduct@semanticinfrastructurelab.org).

### Discussion Forums

**GitHub Discussions** (primary venue):
- 💬 **General Discussion** - Ideas, questions, announcements
- 🔬 **Research** - Academic collaboration, paper feedback
- 💡 **RFC Proposals** - Standards and protocol proposals
- 🛠️ **Tool Development** - Implementation discussions
- 📚 **Documentation** - Improving clarity and accessibility

**GitHub Issues** (project-specific):
- 🐛 Bug reports
- ✨ Feature requests
- 📝 Documentation fixes

---

## Getting Started

### For First-Time Contributors:

1. **Read the [Manifesto](/docs/manifesto)** - Understand SIL's vision (15 min)
2. **Explore the [Reading Guide](/docs/reading-guide)** - Find your path through the docs
3. **Check [Good First Issues](https://github.com/semantic-infrastructure-lab/SIL/labels/good-first-issue)** - Beginner-friendly contributions
4. **Join [Discussions](https://github.com/semantic-infrastructure-lab/SIL/discussions)** - Introduce yourself!

### For Researchers:

1. **Read the [Research Agenda](/docs/sil-research-agenda-year1)** - Current priorities
2. **Review published research:**
   - [RAG as Semantic Manifold Transport](/docs/rag-manifold-transport)
   - [Agent-Help Standard](/docs/agent-help-standard)
3. **Propose collaborations** - Open an RFC or discussion

### For Tool Builders:

1. **Explore production tools:**
   - [reveal](/docs/reveal) - Implement progressive disclosure
   - [morphogen](https://github.com/semantic-infrastructure-lab/morphogen) - Cross-domain computation
   - [tiacad](https://github.com/semantic-infrastructure-lab/tiacad) - Declarative CAD
2. **Implement the [agent-help standard](/docs/agent-help-standard)** in your tools
3. **Share your results** - Help validate and refine the standards

---

## Technical Contribution Process

### Pull Request Guidelines:

**Good PRs:**
- ✅ Small, focused changes (easier to review)
- ✅ Clear description of what and why
- ✅ Tests included (where applicable)
- ✅ Documentation updated
- ✅ Follows existing code style

**PR Description Template:**
```markdown
## What
Brief description of the change

## Why
Problem this solves or motivation

## How
Technical approach taken

## Testing
How was this validated?

## Related
Links to issues, RFCs, or discussions
```

### Commit Message Style:
```
type(scope): brief description

Detailed explanation if needed

Fixes #123
```

**Types:** feat, fix, docs, refactor, test, chore

---

## Recognition & Attribution

**Contributors are valued and credited:**
- All contributors listed in project READMEs
- Significant contributions acknowledged in release notes
- Academic collaborators credited in papers and research
- RFC authors credited in standards documentation

**Intellectual Contributions:**
- Ideas discussed in public forums are attributed to originators
- Citations provided for external research that influences SIL
- Provenance tracking extends to community contributions

---

## Questions?

- 💬 **General questions:** [GitHub Discussions](https://github.com/semantic-infrastructure-lab/SIL/discussions)
- 📧 **Private inquiries:** [hello@semanticinfrastructurelab.org](mailto:hello@semanticinfrastructurelab.org)
- 🐦 **Updates:** Follow [@SemanticInfraLab](https://twitter.com/SemanticInfraLab) (if applicable)

---

## License

By contributing to SIL projects, you agree that your contributions will be licensed under the same license as the project (typically MIT or Apache 2.0 - see individual project licenses).

---

**Welcome to the Semantic Infrastructure Lab community. Let's build the semantic substrate together.**

---

**Last Updated:** 2025-12-03
**Version:** 1.0
