"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { FileUp, Upload, ArrowRight, Loader2, AlertCircle } from "lucide-react"
import { scoreResume } from "@/lib/api"

export function ResumeUploadForm({ onScoreReceived }) {
  const router = useRouter()
  const [resumeFile, setResumeFile] = useState(null)
  const [jobDescription, setJobDescription] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const [error, setError] = useState(null)
  const [useBert, setUseBert] = useState(false)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0]
      if (file.type === "application/pdf") {
        setResumeFile(file)
      }
    }
  }

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      setResumeFile(file)
      setError(null)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!resumeFile || !jobDescription.trim()) return

    setIsProcessing(true)
    setError(null)

    try {
      const scoreResponse = await scoreResume(resumeFile, jobDescription, useBert)

      sessionStorage.setItem("scoreResponse", JSON.stringify(scoreResponse))
      sessionStorage.setItem("resumeFileName", resumeFile.name)

      if (onScoreReceived) {
        onScoreReceived(scoreResponse)
      } else {
        router.push("/results")
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to score resume. Please try again."
      setError(errorMessage)
      setIsProcessing(false)
    }
  }

  const isValid = resumeFile && jobDescription.trim().length > 0

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="flex items-start gap-3 pt-6">
            <AlertCircle className="mt-0.5 h-5 w-5 shrink-0 text-red-600" />
            <div>
              <p className="font-medium text-red-900">Error</p>
              <p className="mt-1 text-sm text-red-800">{error}</p>
            </div>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle className="text-xl">Step 1: Upload Resume</CardTitle>
          <CardDescription>Upload a PDF resume to evaluate the candidate</CardDescription>
        </CardHeader>
        <CardContent>
          <div
            className={`relative rounded-lg border-2 border-dashed transition-colors ${
              dragActive ? "border-primary bg-primary/5" : "border-border bg-muted/30"
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input type="file" id="resume-upload" accept=".pdf" onChange={handleFileChange} className="sr-only" />
            <label
              htmlFor="resume-upload"
              className="flex cursor-pointer flex-col items-center justify-center px-6 py-12 text-center"
            >
              {resumeFile ? (
                <>
                  <FileUp className="mb-4 h-12 w-12 text-primary" />
                  <p className="text-sm font-medium text-foreground">{resumeFile.name}</p>
                  <p className="mt-1 text-xs text-muted-foreground">{(resumeFile.size / 1024).toFixed(2)} KB</p>
                  <Button type="button" variant="link" className="mt-2 h-auto p-0 text-xs">
                    Change file
                  </Button>
                </>
              ) : (
                <>
                  <Upload className="mb-4 h-12 w-12 text-muted-foreground" />
                  <p className="text-sm font-medium text-foreground">Drag & drop a PDF resume here</p>
                  <p className="mt-1 text-xs text-muted-foreground">or click to browse files</p>
                  <Button type="button" variant="secondary" size="sm" className="mt-4">
                    <Upload className="mr-2 h-4 w-4" />
                    Browse Files
                  </Button>
                </>
              )}
            </label>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-xl">Step 2: Job Description</CardTitle>
          <CardDescription>Paste the job description to compare against the resume</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <Label htmlFor="job-description">Job Requirements</Label>
            <Textarea
              id="job-description"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Enter the job description, required skills, qualifications, and responsibilities..."
              className="min-h-[200px] resize-none"
            />
            <p className="text-xs text-muted-foreground">{jobDescription.length} characters</p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Matching Options</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              id="use-bert"
              checked={useBert}
              onChange={(e) => setUseBert(e.target.checked)}
              className="h-4 w-4 rounded border-gray-300 text-primary"
            />
            <Label htmlFor="use-bert" className="cursor-pointer font-normal">
              <span className="font-medium">Use AI semantic matching</span>
              <p className="text-xs text-muted-foreground">Slower but more accurate (uses BERT)</p>
            </Label>
          </div>
        </CardContent>
      </Card>

      <div className="flex justify-end">
        <Button
          type="submit"
          size="lg"
          disabled={!isValid || isProcessing}
          className="bg-accent text-accent-foreground hover:bg-accent/90"
        >
          {isProcessing ? (
            <>
              <Loader2 className="mr-2 h-5 w-5 animate-spin" />
              Processing...
            </>
          ) : (
            <>
              Analyze Resume
              <ArrowRight className="ml-2 h-5 w-5" />
            </>
          )}
        </Button>
      </div>
    </form>
  )
}
