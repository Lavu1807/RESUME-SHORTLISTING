import { ResumeUploadForm } from "@/components/resume-upload-form"
import { FileText } from "lucide-react"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border bg-card">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary">
              <FileText className="h-5 w-5 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-2xl font-semibold text-foreground">Resume Shortlisting</h1>
              <p className="text-sm text-muted-foreground">AI-powered resume screening & candidate matching</p>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl">
          <div className="mb-8 text-center">
            <h2 className="text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
              Screen Candidates Efficiently
            </h2>
            <p className="mt-4 text-pretty text-lg leading-relaxed text-muted-foreground">
              Upload resumes and job descriptions to get instant AI-powered matching scores with detailed skill analysis, experience detection, and hiring recommendations.
            </p>
          </div>

          <ResumeUploadForm />
        </div>
      </main>
    </div>
  )
}
