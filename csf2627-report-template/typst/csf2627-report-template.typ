#let project(
  lab-number: "1",
  group-number: "Group number",
  students: (
    (name: "Name 1", number: "Number 1"),
    (name: "Name 2", number: "Number 2"),
    (name: "Name 3", number: "Number 3"),
  ),
  body,
) = {
  set document(
    title: "Digital Forensics Report Lab" + lab-number,
    author: group-number,
  )

  set text(font: "Liberation Serif", size: 11pt)
  set par(first-line-indent: 0pt, justify: false, leading: 0.48em)

  set heading(numbering: "1.1")
  show heading: set text(font: "Liberation Serif")
  show heading.where(level: 1): set text(size: 14pt, weight: "bold")
  show heading.where(level: 1): set block(above: 1.5em, below: 1em)
  show heading.where(level: 2): set text(size: 12pt, weight: "bold")
  show heading.where(level: 2): set block(above: 1.2em, below: 0.8em)

  set page(
    paper: "a4",
    margin: (top: 2cm, bottom: 2cm, left: 2.5cm, right: 2.5cm),
    footer: context [
      #align(center)[#text(size: 8pt)[CSF -- Lab Assignment I -- Page #counter(page).display()]]
    ],
  )

  align(center)[
    #grid(
      columns: (18%, 76%),
      column-gutter: 6%,
      align: horizon,
      image("figures/NewLogoIST.jpg", width: 100%),
      [
        #text(font: "Liberation Sans", size: 18pt, weight: "bold")[INSTITUTO SUPERIOR TÉCNICO]\
        #v(0.2cm)
        #text(font: "Liberation Sans", size: 12pt)[Departamento de Engenharia Informática]
      ],
    )

    #v(2.3cm)
    #text(font: "Liberation Sans", size: 22pt, weight: "bold")[Forensics Cyber-Security]\
    #v(0.35cm)
    #text(size: 12pt)[MEIC, METI]

    #v(1fr)
    #text(size: 20pt, weight: "bold")[Digital Forensics Report]\
    #v(0.4cm)
    #text(size: 16pt, weight: "bold")[Lab Assignment I -- Operation DeepFISH -- Stage I]

    #v(1.2cm)
    #table(
      columns: (20%, 1fr, 20%),
      inset: 6pt,
      align: (left, left, right),
      stroke: none,
      [*Group:*], table.cell(colspan: 2)[#group-number],
      [*Student 1:*], [Name 1], [Number 1],
      [*Student 2:*], [Name 2], [Number 2],
      [*Student 3:*], [Name 3], [Number 3],
    )

    #v(1fr)
    #text(size: 12pt)[2026/2027]
  ]

  pagebreak()
  body
}

#show: project.with()

= Acquired artifacts <acquired-artifacts>

// Include relevant acquired or recovered artifacts. For submitted artifacts,
// identify the filename, SHA-256 hash and source/provenance where applicable.
#table(
  columns: (25%, 22%, 1fr),
  align: center,
  stroke: 0.5pt,
  table.header([*Name*], [*Source / Provenance*], [*SHA-256 Value*]),
  table.cell(inset: 30pt)[], table.cell(inset: 30pt)[], table.cell(inset: 30pt)[],
)

= Report of all findings (Investigation and Evidence Analysis) <report-of-all-findings>

_Document the relevant findings of the investigation._

// TODO: Include examination of the suspicious message and URL, relevant
// web/file analysis, concealed artifacts, extraction methodology, tools,
// reproducible commands and relevant timestamps. Clearly distinguish observed
// evidence from forensic inference.
#line(length: 0pt)

= Analysis of relevant findings <analysis-of-relevant-findings>

== Nature of the incident <nature-of-the-incident>

_(a) Did you find evidence that the reported activity was part of a scam? If so, describe the nature of the scam and reconstruct how it was conducted. (b) Did you uncover any additional concealed artifacts during your investigation? If so, explain how these artifacts were concealed and describe the methodology used to recover them. For both (a) and (b), support your conclusions with the relevant evidence identified during the investigation.)_

// TODO: Answer based on the evidence obtained. Distinguish established facts
// from conclusions or inferences.
#line(length: 0pt)

== Interpretation of the evidence <interpretation-of-the-evidence>

_Focusing on the recovered concealed material, can you identify relationships among the recovered items, explain what they may represent, and formulate a supported hypothesis about their significance to the case? Clearly identify which parts of your interpretation are established by evidence and which remain inferential._

// TODO: Include the concealed material, relationships, interpretation,
// supported hypothesis and relevant chronology/timeline.
#line(length: 0pt)

== Attribution and next investigative steps <attribution-and-next-investigative-steps>

_Does the available evidence support any conclusion about the identity of the person or persons responsible for the scam or any other suspicious activity uncovered? Discuss the strengths and weaknesses of the attribution evidence you have found. Provide recommendations to SI regarding the next investigative steps, including any additional evidence that should be preserved or obtained before further action is taken._

// TODO: Address attribution, strength of evidence, limitations, uncertainty,
// recommended next steps and evidence that SI should preserve or obtain.
#line(length: 0pt)

= Use of Artificial Intelligence <ai>

_Did you use Artificial Intelligence (AI) tools in the preparation of this report? If so, identify the tool(s) used and briefly state the purpose(s) for which they were used._

// TODO: Answer "No", or identify the AI tool(s) used and their purpose(s).
#line(length: 0pt)

= Appendices <appendices>

// TODO: Attach relevant supporting evidence, screenshots, commands, tool
// outputs or other material useful to substantiate or reproduce the findings.
#line(length: 0pt)
