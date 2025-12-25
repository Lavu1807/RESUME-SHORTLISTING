"use client"

import type React from "react"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { CheckCircle, XCircle, User, Briefcase, Award, Brain, Target, Code, Calendar } from "lucide-react"
import type { ScoreResponse } from "@/lib/api"

interface ResultsViewProps {
  scoreData?: ScoreResponse
}

export function ResultsView({ scoreData: initialData }: ResultsViewProps) {
  const [scoreData, setScoreData] = useState<ScoreResponse | null>(initialData || null)
  const [resumeFileName, setResumeFileName] = useState("")
  const [isLoading, setIsLoading] = useState(!initialData)

  useEffect(() => {
    if (initialData) return

    // Load from sessionStorage if not passed as prop
    const storedScore = sessionStorage.getItem("scoreResponse")
    const storedFileName = sessionStorage.getItem("resumeFileName")

    if (storedScore) {
      try {
        setScoreData(JSON.parse(storedScore))
        setResumeFileName(storedFileName || "Resume")
      } catch {
        // Failed to parse
      }
    }
    setIsLoading(false)
  }, [initialData])

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Card>
          <CardContent className="flex items-center justify-center py-12">
            <p className="text-muted-foreground">Loading results...</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (!scoreData) {
    return (
      <div className="space-y-6">
        <Card className="border-yellow-200 bg-yellow-50">
          <CardContent className="pt-6">
            <p className="text-sm text-yellow-800">No results found. Please upload a resume to get started.</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  const candidateName = resumeFileName.replace(/\.(pdf|docx)$/i, "")
  const isSelected = scoreData.score >= 70
  const skillsMatchCount = scoreData.skills_matched.length

  const getScoreColor = (score: number) => {
    if (score >= 85) return "text-green-600"
    if (score >= 70) return "text-yellow-600"
    return "text-red-600"
  }

  const getProgressColor = (score: number) => {
    if (score >= 85) return "bg-green-600"
    if (score >= 70) return "bg-yellow-600"
    return "bg-red-600"
  }

  return (
    <div className="space-y-6">
      <Card className="border-2">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
                <User className="h-6 w-6 text-primary" />
              </div>
              <div>
                <CardTitle className="text-2xl">{candidateName}</CardTitle>
                <CardDescription className="mt-1">Resume Scoring Summary</CardDescription>
              </div>
            </div>
            <Badge
              variant={isSelected ? "default" : "secondary"}
              className={`text-sm ${
                isSelected ? "bg-green-600 text-white hover:bg-green-700" : "bg-red-600 text-white hover:bg-red-700"
              }`}
            >
              {isSelected ? (
                <>
                  <CheckCircle className="mr-1.5 h-4 w-4" />
                  Recommended
                </>
              ) : (
                <>
                  <XCircle className="mr-1.5 h-4 w-4" />
                  Below Threshold
                </>
              )}
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <div className="mb-2 flex items-center justify-between">
                <span className="text-sm font-medium text-foreground">Overall Match Score</span>
                <span className={`text-3xl font-bold ${getScoreColor(scoreData.score)}`}>{scoreData.score}%</span>
              </div>
              <div className="relative h-3 overflow-hidden rounded-full bg-secondary">
                <div
                  className={`h-full transition-all duration-1000 ${getProgressColor(scoreData.score)}`}
                  style={{ width: `${scoreData.score}%` }}
                />
              </div>
            </div>

            <div className="pt-4">
              <p className="text-sm leading-relaxed text-muted-foreground">
                {isSelected
                  ? "This candidate shows strong alignment with the job requirements. Their technical background and skills closely match the position. Recommended for further review."
                  : "This candidate does not fully meet the minimum scoring threshold. Their experience or skills may not align well with the specific requirements of this position."}
              </p>
            </div>

            <div className="pt-4 text-xs text-muted-foreground">
              <p>Analyzed using: <strong>{scoreData.method_used}</strong> method</p>
              {scoreData.explanation && <p className="mt-1">{scoreData.explanation}</p>}
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-100 text-blue-600">
                <Code className="h-4 w-4" />
              </div>
              <CardTitle className="text-base">Skills Matched</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="text-2xl font-bold text-blue-600">{skillsMatchCount}</div>
              {scoreData.skills_matched.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {scoreData.skills_matched.map((skill) => (
                    <Badge key={skill} variant="secondary" className="bg-blue-100 text-blue-700">
                      {skill}
                    </Badge>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">No matching skills detected</p>
              )}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-green-100 text-green-600">
                <Calendar className="h-4 w-4" />
              </div>
              <CardTitle className="text-base">Experience</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="text-2xl font-bold text-green-600">{scoreData.years_experience.toFixed(1)}</div>
              <p className="text-sm text-muted-foreground">years estimated from resume</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Top Job Keywords</CardTitle>
          <CardDescription>Keywords from job description ranked by importance</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {scoreData.top_keywords.map((keyword) => (
              <Badge key={keyword} variant="outline">
                {keyword}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Analysis Details</CardTitle>
          <CardDescription>Resume and Job Description Statistics</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between border-b pb-2">
              <span className="text-muted-foreground">Resume Characters:</span>
              <span className="font-medium">{scoreData.resume_char_count.toLocaleString()}</span>
            </div>
            <div className="flex justify-between border-b pb-2">
              <span className="text-muted-foreground">Job Description Characters:</span>
              <span className="font-medium">{scoreData.job_char_count.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Matching Algorithm:</span>
              <span className="font-medium">{scoreData.method_used}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
