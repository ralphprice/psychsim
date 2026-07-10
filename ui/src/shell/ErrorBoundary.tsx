// ErrorBoundary — contains a render/runtime throw to the active tab-panel instead of letting it
// unmount the whole console (the black-screen failure mode). The shell chrome (telemetry, tab bar,
// control rail) stays live; the panel shows a recoverable message and a reset. `resetKey` clears the
// error when the surrounding context changes (e.g. switching tabs), so a transient fault self-heals.

import { Component, type ErrorInfo, type ReactNode } from "react";

interface Props {
  children: ReactNode;
  resetKey?: unknown;
}
interface State {
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    // Surface it for the console, but do not re-throw — containment is the whole point.
    console.error("panel crashed:", error, info.componentStack);
  }

  componentDidUpdate(prev: Props) {
    if (prev.resetKey !== this.props.resetKey && this.state.error) {
      this.setState({ error: null });
    }
  }

  render() {
    const { error } = this.state;
    if (error) {
      return (
        <div className="panel-error" role="alert">
          <div className="panel-error-title">This panel hit an error.</div>
          <div className="panel-error-msg">{error.message}</div>
          <button onClick={() => this.setState({ error: null })}>Retry</button>
        </div>
      );
    }
    return this.props.children;
  }
}
