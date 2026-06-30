import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import { VERBS, Verb } from "./verbs";

type FeedbackKind = "ready" | "correct" | "wrong" | "skipped" | "revealed";

type LastAnswer = {
  result: "Correct" | "Wrong" | "Skipped" | "Revealed";
  english: string;
  userAnswer: string;
  correctAnswer: string;
};

const STARTING_FEEDBACK = "Press Enter or click Check.";

function shuffleVerbs(verbs: Verb[]) {
  const shuffled = [...verbs];

  for (let index = shuffled.length - 1; index > 0; index -= 1) {
    const randomIndex = Math.floor(Math.random() * (index + 1));
    [shuffled[index], shuffled[randomIndex]] = [shuffled[randomIndex], shuffled[index]];
  }

  return shuffled;
}

function cleanText(text: string) {
  return text
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}

function putBackSoon(queue: Verb[], verb: Verb) {
  const nextQueue = [...queue];
  const position = Math.min(Math.floor(Math.random() * 4) + 2, nextQueue.length);
  nextQueue.splice(position, 0, verb);
  return nextQueue;
}

function App() {
  const [score, setScore] = useState(0);
  const [attempts, setAttempts] = useState(0);
  const [streak, setStreak] = useState(0);
  const [queue, setQueue] = useState<Verb[]>(() => shuffleVerbs(VERBS));
  const [currentVerb, setCurrentVerb] = useState<Verb | null>(null);
  const [answer, setAnswer] = useState("");
  const [answerFinished, setAnswerFinished] = useState(false);
  const [feedback, setFeedback] = useState(STARTING_FEEDBACK);
  const [feedbackKind, setFeedbackKind] = useState<FeedbackKind>("ready");
  const [lastAnswers, setLastAnswers] = useState<LastAnswer[]>([]);

  const inputRef = useRef<HTMLInputElement>(null);

  const accuracy = useMemo(() => {
    if (attempts === 0) {
      return 0;
    }

    return Math.round((score / attempts) * 100);
  }, [attempts, score]);

  useEffect(() => {
    nextQuestion();
  }, []);

  useEffect(() => {
    if (!answerFinished) {
      inputRef.current?.focus();
    }
  }, [answerFinished, currentVerb]);

  function drawFromQueue(existingQueue: Verb[]) {
    const readyQueue = existingQueue.length > 0 ? existingQueue : shuffleVerbs(VERBS);
    const [nextVerb, ...remainingQueue] = readyQueue;
    setCurrentVerb(nextVerb);
    setQueue(remainingQueue);
  }

  function nextQuestion() {
    drawFromQueue(queue);
    setAnswer("");
    setAnswerFinished(false);
    setFeedback(STARTING_FEEDBACK);
    setFeedbackKind("ready");
  }

  function addLastAnswer(entry: LastAnswer) {
    setLastAnswers((previousAnswers) => [entry, ...previousAnswers].slice(0, 5));
  }

  function finishAnswer() {
    setAnswerFinished(true);
  }

  function checkAnswer() {
    if (!currentVerb || answerFinished) {
      return;
    }

    const userAnswer = answer;
    const isCorrect = cleanText(userAnswer) === cleanText(currentVerb.dutch);

    setAttempts((currentAttempts) => currentAttempts + 1);

    if (isCorrect) {
      setScore((currentScore) => currentScore + 1);
      setStreak((currentStreak) => currentStreak + 1);
      setQueue((currentQueue) => [...currentQueue, currentVerb]);
      setFeedback(`Correct! ${currentVerb.dutch} means ${currentVerb.english}.`);
      setFeedbackKind("correct");
      addLastAnswer({
        result: "Correct",
        english: currentVerb.english,
        userAnswer,
        correctAnswer: currentVerb.dutch,
      });
    } else {
      setStreak(0);
      setQueue((currentQueue) => putBackSoon(currentQueue, currentVerb));
      setFeedback(`Not quite. The answer is: ${currentVerb.dutch}`);
      setFeedbackKind("wrong");
      addLastAnswer({
        result: "Wrong",
        english: currentVerb.english,
        userAnswer,
        correctAnswer: currentVerb.dutch,
      });
    }

    finishAnswer();
  }

  function skipQuestion() {
    if (!currentVerb) {
      return;
    }

    if (answerFinished) {
      nextQuestion();
      return;
    }

    setStreak(0);
    setQueue((currentQueue) => putBackSoon(currentQueue, currentVerb));
    setFeedback(`Skipped. The answer is: ${currentVerb.dutch}`);
    setFeedbackKind("skipped");
    addLastAnswer({
      result: "Skipped",
      english: currentVerb.english,
      userAnswer: "-",
      correctAnswer: currentVerb.dutch,
    });
    finishAnswer();
  }

  function revealAnswer() {
    if (!currentVerb || answerFinished) {
      return;
    }

    setStreak(0);
    setQueue((currentQueue) => putBackSoon(currentQueue, currentVerb));
    setFeedback(`Answer revealed: ${currentVerb.dutch}`);
    setFeedbackKind("revealed");
    addLastAnswer({
      result: "Revealed",
      english: currentVerb.english,
      userAnswer: "-",
      correctAnswer: currentVerb.dutch,
    });
    finishAnswer();
  }

  function resetSession() {
    const freshQueue = shuffleVerbs(VERBS);
    const [nextVerb, ...remainingQueue] = freshQueue;

    setScore(0);
    setAttempts(0);
    setStreak(0);
    setLastAnswers([]);
    setCurrentVerb(nextVerb);
    setQueue(remainingQueue);
    setAnswer("");
    setAnswerFinished(false);
    setFeedback(STARTING_FEEDBACK);
    setFeedbackKind("ready");
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (answerFinished) {
      nextQuestion();
    } else {
      checkAnswer();
    }
  }

  return (
    <main className="app-shell">
      <section className="hero">
        <p className="eyebrow">English to Dutch infinitives</p>
        <h1>Dutch Verb Sprint</h1>
      </section>

      <section className="stats-grid" aria-label="Session statistics">
        <div className="stat-card">
          <span>Score</span>
          <strong>{score}</strong>
        </div>
        <div className="stat-card">
          <span>Attempts</span>
          <strong>{attempts}</strong>
        </div>
        <div className="stat-card">
          <span>Accuracy</span>
          <strong>{accuracy}%</strong>
        </div>
        <div className="stat-card">
          <span>Streak</span>
          <strong>{streak}</strong>
        </div>
      </section>

      <form className={`flashcard ${feedbackKind}`} onSubmit={handleSubmit}>
        <p className="prompt-label">Translate this verb</p>
        <h2>{currentVerb?.english ?? "Loading..."}</h2>

        <label className="answer-label" htmlFor="answer">
          Dutch infinitive
        </label>
        <input
          id="answer"
          ref={inputRef}
          value={answer}
          onChange={(event) => setAnswer(event.target.value)}
          disabled={answerFinished}
          autoComplete="off"
          autoCapitalize="none"
          spellCheck="false"
          placeholder="Type your answer"
        />

        <div className="feedback" role="status" aria-live="polite">
          {feedback}
        </div>

        <div className="button-row">
          <button type="submit" className="primary-button" disabled={answerFinished}>
            Check
          </button>
          <button type="button" onClick={nextQuestion}>
            Next
          </button>
          <button type="button" onClick={skipQuestion}>
            Skip
          </button>
          <button type="button" onClick={revealAnswer} disabled={answerFinished}>
            Reveal Answer
          </button>
          <button type="button" onClick={resetSession}>
            Reset Session
          </button>
        </div>
      </form>

      <section className="summary-panel">
        <div>
          <h2>Last 5 answers</h2>
          <p>{VERBS.length} verbs in this sprint list</p>
        </div>

        {lastAnswers.length === 0 ? (
          <p className="empty-summary">No answers yet.</p>
        ) : (
          <ol className="answer-list">
            {lastAnswers.map((entry, index) => (
              <li key={`${entry.english}-${entry.result}-${index}`}>
                <strong>{entry.result}</strong>
                <span>{entry.english}</span>
                <span>
                  {entry.userAnswer} / {entry.correctAnswer}
                </span>
              </li>
            ))}
          </ol>
        )}
      </section>
    </main>
  );
}

export default App;
